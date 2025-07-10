import json
from pathlib import Path
from dotenv import load_dotenv
import os
import torch
from transformers import pipeline

# Load environment variables
load_dotenv()
PROMPT_FILE = "prompts.json"
OUTPUT_DIR = Path("kfp_eval_samples")
OUTPUT_DIR.mkdir(exist_ok=True)

# Load prompts
with open(PROMPT_FILE) as f:
    prompts = json.load(f)

# Initialize the LLaMA 3.1 model pipeline
print("🔧 Loading LLaMA 3.1 pipeline...")
llama_pipeline = pipeline(
    "text-generation",
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto"
)

def generate_with_llama(prompt):
    # Format as a chat message
    messages = [
        {"role": "system", "content": "You are an MLOps expert who writes correct and complete Kubeflow Pipelines."},
        {"role": "user", "content": prompt}
    ]
    try:
        output = llama_pipeline(messages, max_new_tokens=1024, do_sample=False, temperature=0.2)
        return output[0]["generated_text"]
    except Exception as e:
        return f"# LLaMA generation failed: {e}"

# Generate using only LLaMA for now
for item in prompts:
    prompt = item['structured_prompt']
    sample_id = item['repo'].split("/")[-1]  # Use repo name as sample ID

    print(f"🦙 Generating for sample {sample_id} using LLaMA 3.1...")
    code = generate_with_llama(prompt)
    file_path = OUTPUT_DIR / f"sample_{sample_id}_llama.py"
    file_path.write_text(code)

print("✅ LLaMA 3.1 KFP code generation completed.")
