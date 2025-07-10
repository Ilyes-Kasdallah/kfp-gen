import json
from pathlib import Path
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
hf_token = os.getenv("HF_TOKEN")
hf_client = InferenceClient(token=hf_token)

# Config
PROMPT_FILE = "prompts.json"
OUTPUT_DIR = Path("kfp_eval_samples")
LLM_AGENTS = ["gpt4", "llama", "qwen", "alphaevolve"]
OUTPUT_DIR.mkdir(exist_ok=True)

# Load prompts
with open(PROMPT_FILE) as f:
    prompts = json.load(f)

# Model mapping for Hugging Face
HF_MODELS = {
    "llama": "meta-llama/Meta-Llama-3-8B-Instruct",
    "qwen": "Qwen/Qwen2.5-1.8B-Chat",
    "alphaevolve": "deepseek-ai/DeepSeek-Coder-6.7B-Instruct"
}

def generate_with_llm(prompt, agent):
    if agent == "gpt4":
        print(f"🧠 Calling GPT-4...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an MLOps expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        return response.choices[0].message["content"]

    elif agent in HF_MODELS:
        print(f"🤖 Calling Hugging Face model: {HF_MODELS[agent]}")
        return hf_client.text_generation(
            prompt=prompt,
            model=HF_MODELS[agent],
            max_new_tokens=1024,
            temperature=0.2,
            do_sample=False
        )

    else:
        return "# Unknown LLM agent"

# Loop through prompts
for item in prompts:
    prompt = item['structured_prompt']
    sample_id = item['repo'].split("/")[-1]  # Use repo name as sample ID

    for agent in LLM_AGENTS:
        try:
            code = generate_with_llm(prompt, agent)
            file_path = OUTPUT_DIR / f"sample_{sample_id}_{agent}.py"
            file_path.write_text(code)
        except Exception as e:
            print(f"❌ Failed on sample {sample_id}, agent {agent}: {e}")

print("✅ All LLM outputs generated.")
