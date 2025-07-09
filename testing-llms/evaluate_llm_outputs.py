import os
import difflib
import pandas as pd
from pathlib import Path
import time

# ---- Setup ----
SAMPLES_DIR = Path("kfp_eval_samples")
LLM_AGENTS = ["gpt4", "llama", "qwen", "alphaevolve"]
results = []

# ---- Helpers ----
def compute_similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def score_generated_code(code, similarity, reference):
    score = 0
    if "@dsl.pipeline" in code or "dsl.pipeline" in code:
        score += 2  # correct structure
    if "kfp.components" in code or "dsl.ContainerOp" in code or "@dsl.component" in code:
        score += 2  # uses KFP constructs
    if similarity > 0.7:
        score += 2  # high similarity
    if "def" in code and "#" in code:
        score += 1  # some comments
    if "load_component_from_url" in code or "create_pipeline" in code:
        score += 2  # shows knowledge of reuse/generation
    return score

# ---- Main Evaluation Loop ----
for prompt_file in SAMPLES_DIR.glob("sample_*_prompt.txt"):
    i = prompt_file.stem.split("_")[1]
    ref_path = SAMPLES_DIR / f"sample_{i}_reference.py"
    
    if not ref_path.exists():
        continue

    with open(ref_path) as f:
        reference = f.read()

    for agent in LLM_AGENTS:
        agent_file = SAMPLES_DIR / f"sample_{i}_{agent}.py"
        if not agent_file.exists():
            continue

        with open(agent_file) as f:
            generated = f.read()

        start = time.time()
        similarity = compute_similarity(reference, generated)
        latency = time.time() - start
        score = score_generated_code(generated, similarity, reference)

        results.append({
            "Sample": int(i),
            "Agent": agent,
            "Similarity (%)": round(similarity * 100, 2),
            "Latency (s)": round(latency, 2),
            "Score (/10)": score
        })

# ---- Save and Show Results ----
df = pd.DataFrame(results)
df.sort_values(by=["Sample", "Agent"], inplace=True)

df.to_csv(SAMPLES_DIR / "llm_pipeline_eval.csv", index=False)
df.to_excel(SAMPLES_DIR / "llm_pipeline_eval.xlsx", index=False)

print("✅ Evaluation completed and saved to:")
print(f"  - {SAMPLES_DIR}/llm_pipeline_eval.csv")
print(f"  - {SAMPLES_DIR}/llm_pipeline_eval.xlsx")
