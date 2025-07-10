import os
from pathlib import Path
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import pandas as pd

SAMPLES_DIR = Path("kfp_eval_samples")
LLM_AGENTS = ["gpt4", "llama", "qwen", "alphaevolve"]
results = []

smoothie = SmoothingFunction().method4

for prompt_file in SAMPLES_DIR.glob("sample_*_prompt.txt"):
    sample_id = prompt_file.stem.split("_")[1]
    ref_path = SAMPLES_DIR / f"sample_{sample_id}_reference.py"

    if not ref_path.exists():
        continue

    reference = ref_path.read_text().split()

    for agent in LLM_AGENTS:
        gen_path = SAMPLES_DIR / f"sample_{sample_id}_{agent}.py"
        if not gen_path.exists():
            continue

        candidate = gen_path.read_text().split()
        bleu = sentence_bleu([reference], candidate, smoothing_function=smoothie)

        results.append({
            "Sample": int(sample_id),
            "Agent": agent,
            "BLEU Score": round(bleu * 100, 2)
        })

# Save results
if results:
    df = pd.DataFrame(results)
    df.sort_values(by=["Sample", "Agent"], inplace=True)

    df.to_csv(SAMPLES_DIR / "llm_bleu_scores.csv", index=False)
    df.to_excel(SAMPLES_DIR / "llm_bleu_scores.xlsx", index=False)

    print("✅ BLEU score evaluation complete.")
else:
    print("⚠️ No BLEU scores calculated. Check if your sample/reference/generated files exist.")
