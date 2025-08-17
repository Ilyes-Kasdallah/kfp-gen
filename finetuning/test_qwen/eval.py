#!/usr/bin/env python3
"""
Generate KFP pipelines with your fine-tuned Qwen and evaluate them with:
- pylint (Python code quality)
- kube-linter (compiled YAML checks)
- METEOR (text similarity vs. reference in the test split)

Data source:
  --hf-path points to a HuggingFace dataset saved with load_from_disk().
  Examples:
    finetuning/data/prompts_dataset/test           (Dataset)
    finetuning/data/prompts_dataset                (DatasetDict with train/test)
    finetuning/data/data/prompts_dataset/test      (if you have the extra 'data' level)

The script auto-detects whether the path is a Dataset or DatasetDict and selects the
'test' split when available.

Expected fields (heuristic; first match wins):
  prompt:  ["prompt", "instruction", "input", "messages", "text"]
  ref:     ["completion", "reference", "response", "output", "kfp_code"]

Outputs (default out-dir = finetuning/testing_qwen/runs/exp1):
  runs/exp1/gen/<id>.py
  runs/exp1/yaml/<id>.yaml
  runs/exp1/logs/<id>_pylint.txt
  runs/exp1/logs/<id>_kubelinter.json
  runs/exp1/results.csv
  runs/exp1/results.json
"""
import argparse, json, os, re, subprocess, sys, importlib.util, csv, pathlib, textwrap
from dataclasses import dataclass, asdict
from io import StringIO
from typing import Dict, Any, List, Tuple, Optional

# --- Model / generation ---
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- HuggingFace datasets ---
from datasets import load_from_disk, Dataset, DatasetDict

# --- Lint & metrics ---
from pylint.lint import Run as PylintRun
from pylint.reporters.text import TextReporter
import nltk
from nltk.translate.meteor_score import meteor_score

# --- KFP compile ---
from kfp import compiler as kfp_compiler

# Ensure NLTK data (quiet)
nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)

@dataclass
class Row:
    id: str
    gen_path: str
    yaml_path: str
    pylint_score: float
    pylint_errors: int
    kubelinter_issues: int
    meteor: float
    notes: str

SYS_PROMPT = (
    "You are an expert ML engineer. Output a COMPLETE Kubeflow Pipelines v2 "
    "Python file. Use 'from kfp import dsl', @dsl.component for steps, "
    "@dsl.pipeline for the pipeline entrypoint, provide resource requests/limits, "
    "avoid markdown fences and make the file importable."
)

STOP_PATTERNS = [r"^```", r"^# End", r"^if __name__ == ['\"]__main__['\"]:"]

# ---------- Model ----------
def load_model(model_path: str):
    # Prefer fast tokenizer; fall back to slow if the Rust tokenizer can't parse tokenizer.json
    try:
        tok = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    except Exception:
        tok = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, use_fast=False)

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True,
    )
    return tok, model

def generate_code(tok, model, user_prompt: str, max_new_tokens=1200, temperature=0.2, top_p=0.9) -> str:
    full = f"{SYS_PROMPT}\n\nUser task:\n{user_prompt}\n\nPython file start:\n"
    inputs = tok(full, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            eos_token_id=tok.eos_token_id,
        )
    text = tok.decode(out[0], skip_special_tokens=True)
    gen = text.split("Python file start:")[-1].strip()

    # Trim at common stop patterns and remove markdown fences if present
    lines = []
    for line in gen.splitlines():
        if any(re.match(p, line) for p in STOP_PATTERNS):
            break
        lines.append(line)
    gen = "\n".join(lines)
    gen = re.sub(r"^```(?:python)?", "", gen, flags=re.MULTILINE).replace("```", "").strip()

    # Ensure required imports
    if "from kfp import dsl" not in gen:
        gen = "from kfp import dsl\nfrom kfp.dsl import component\n\n" + gen
    return gen

# ---------- Lint / Compile / Metrics ----------
def pylint_file(path: str) -> Tuple[float, int, str]:
    buf = StringIO()
    reporter = TextReporter(output=buf)
    _ = PylintRun(
        [path, "--score=y", "--disable=C0114,C0115,C0116,R0902,R0903,R0913,R0914"],
        reporter=reporter, do_exit=False
    )
    report = buf.getvalue()
    score_match = re.search(r"rated at ([\-0-9.]+)/10", report)
    score = float(score_match.group(1)) if score_match else 0.0
    errors = len(re.findall(r": (error|fatal):", report))
    return score, errors, report

def compile_kfp(pyfile: str, out_yaml: str) -> None:
    spec = importlib.util.spec_from_file_location("generated_pipeline", pyfile)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    compiled = False
    for _, obj in vars(mod).items():
        if callable(obj):
            try:
                kfp_compiler.Compiler().compile(obj, out_yaml)
                compiled = True
                break
            except Exception:
                continue
    if not compiled:
        raise RuntimeError("No valid @dsl.pipeline function could be compiled.")

def kube_lint(yaml_path: str) -> Dict[str, Any]:
    try:
        proc = subprocess.run(
            ["kube-linter", "lint", "--format", "json", yaml_path],
            capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        raise RuntimeError("kube-linter not found in PATH")
    # kube-linter returns 0 (no issues) or 3 (issues found)
    if proc.returncode not in (0, 3):
        raise RuntimeError(proc.stderr.strip() or "kube-linter failed")
    data = json.loads(proc.stdout or "{}")
    issues = len(data.get("Reports", [])) if isinstance(data, dict) else 0
    return {"issues": issues, "raw": data}

def meteor_vs_ref(generated_text: str, reference_text: str) -> float:
    if not reference_text:
        return 0.0
    return float(meteor_score([reference_text], generated_text))

# ---------- Data loading ----------
def _extract_prompt_and_ref(example: dict) -> Tuple[str, str]:
    """Heuristic extraction to cover common SFT schemas."""
    # prompt
    prompt = (
        example.get("prompt")
        or example.get("instruction")
        or example.get("input")
        or ""
    )

    # messages (chat-style)
    if not prompt and "messages" in example and isinstance(example["messages"], list):
        # concatenate roles/content for a single prompt text
        prompt = "\n".join(
            f"{m.get('role', 'user')}: {m.get('content','')}"
            for m in example["messages"]
        )

    # single-field text (some datasets pack everything in 'text')
    if not prompt and "text" in example:
        prompt = str(example["text"])

    # reference / completion
    ref = (
        example.get("completion")
        or example.get("reference")
        or example.get("response")
        or example.get("output")
        or example.get("kfp_code")
        or ""
    )
    return prompt, ref

def load_hf_test_split(path: str) -> Dataset:
    """
    Accepts:
      - path to a Dataset folder (e.g., prompts_dataset/test)
      - path to a DatasetDict folder (e.g., prompts_dataset) -> picks 'test' if present,
        otherwise 'validation', otherwise first available split.
    """
    obj = load_from_disk(path)
    if isinstance(obj, Dataset):
        return obj
    if isinstance(obj, DatasetDict):
        # Prefer 'test' -> 'validation' -> first split
        for name in ("test", "validation"):
            if name in obj:
                return obj[name]
        first = next(iter(obj.keys()))
        return obj[first]
    raise ValueError("Unsupported HuggingFace dataset object type.")

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-path", required=True, help="Path/HF id for your fine-tuned Qwen.")
    ap.add_argument("--hf-path", required=True, help="Path to HF dataset on disk (test split or parent DatasetDict).")
    ap.add_argument("--out-dir", default="finetuning/testing_qwen/runs/exp1", help="Output directory for results.")
    ap.add_argument("--max-samples", type=int, default=None, help="Limit number of evaluated samples.")
    ap.add_argument("--save-refs", action="store_true", help="Also write extracted references to refs/<id>.py (for inspection).")
    args = ap.parse_args()

    # Prepare dirs
    gen_dir = os.path.join(args.out_dir, "gen")
    yaml_dir = os.path.join(args.out_dir, "yaml")
    logs_dir = os.path.join(args.out_dir, "logs")
    for d in (args.out_dir, gen_dir, yaml_dir, logs_dir):
        os.makedirs(d, exist_ok=True)

    # Load model & test dataset
    tok, model = load_model(args.model_path)
    test_ds = load_hf_test_split(args.hf_path)
    if args.max_samples is not None:   # type: ignore[attr-defined]
        test_ds = test_ds.select(range(min(len(test_ds), args.max_samples)))

    rows: List[Row] = []
    for idx, ex in enumerate(test_ds):
        sid = str(ex.get("id", f"sample{idx}"))
        prompt, ref_text = _extract_prompt_and_ref(ex)
        if not prompt:
            rows.append(Row(sid, "", "", 0.0, 0, 0, 0.0, "[skip:no_prompt]"))
            continue

        gen_py = os.path.join(gen_dir, f"{sid}.py")
        out_yaml = os.path.join(yaml_dir, f"{sid}.yaml")
        note = ""

        # Generate code
        try:
            code = generate_code(tok, model, prompt)
            with open(gen_py, "w", encoding="utf-8") as w:
                w.write(code)
        except Exception as ex:
            rows.append(Row(sid, "", "", 0.0, 0, 0, 0.0, f"[gen_fail:{ex}]"))
            continue

        # pylint
        try:
            score, errs, rep = pylint_file(gen_py)
            with open(os.path.join(logs_dir, f"{sid}_pylint.txt"), "w", encoding="utf-8") as w:
                w.write(rep)
        except Exception as ex:
            score, errs = 0.0, 0
            note += f"[pylint_fail:{ex}] "

        # compile to yaml
        try:
            compile_kfp(gen_py, out_yaml)
        except Exception as ex:
            rows.append(Row(sid, os.path.abspath(gen_py), "", score, errs, 0, 0.0, note + f"[compile_fail:{ex}]"))
            continue

        # kube-linter
        try:
            kl = kube_lint(out_yaml)
            issues = int(kl.get("issues", 0))
            with open(os.path.join(logs_dir, f"{sid}_kubelinter.json"), "w", encoding="utf-8") as w:
                json.dump(kl, w, indent=2)
        except Exception as ex:
            issues = 0
            note += f"[kubelinter_fail:{ex}] "

        # METEOR
        try:
            with open(gen_py, "r", encoding="utf-8") as r:
                gen_txt = r.read()
            meteor_val = meteor_vs_ref(gen_txt, ref_text)
            if args.save_refs and ref_text:   # type: ignore[attr-defined]
                refs_dir = os.path.join(args.out_dir, "refs")
                os.makedirs(refs_dir, exist_ok=True)
                with open(os.path.join(refs_dir, f"{sid}.py"), "w", encoding="utf-8") as w:
                    w.write(ref_text)
        except Exception as ex:
            meteor_val = 0.0
            note += f"[meteor_fail:{ex}] "

        rows.append(
            Row(
                id=sid,
                gen_path=os.path.abspath(gen_py),
                yaml_path=os.path.abspath(out_yaml),
                pylint_score=score,
                pylint_errors=errs,
                kubelinter_issues=issues,
                meteor=meteor_val,
                notes=note.strip(),
            )
        )

    # Write results
    csv_path = os.path.join(args.out_dir, "results.csv")
    json_path = os.path.join(args.out_dir, "results.json")
    with open(csv_path, "w", newline="", encoding="utf-8") as c:
        fields = ["id","gen_path","yaml_path","pylint_score","pylint_errors","kubelinter_issues","meteor","notes"]
        w = csv.DictWriter(c, fieldnames=fields); w.writeheader()
        for r in rows: w.writerow(asdict(r))
    with open(json_path, "w", encoding="utf-8") as j:
        json.dump([asdict(r) for r in rows], j, indent=2)

    print(f"CSV: {csv_path}\nJSON: {json_path}\nGen: {gen_dir}\nYAML: {yaml_dir}\nLogs: {logs_dir}")

if __name__ == "__main__":
    main()
