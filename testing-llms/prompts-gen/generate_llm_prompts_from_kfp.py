import json
import time
import google.generativeai as genai

# 🔐 Configure Gemini API key
import os

api_key = os.getenv("GITHUB_TOKEN")
genai.configure(api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# Load dataset
with open("kfp_pipeline_snippets copy.json", "r", encoding="utf-8") as f:
    kfp_data = json.load(f)

# Prompt to Gemini
def generate_structured_prompt(code, file):
    gemini_prompt = f"""
You are an MLOps expert and prompt engineer.

I will give you a Python file that defines a Kubeflow Pipeline using the `@dsl.pipeline` and `@component` decorators.

Your task is to write a clear and structured **prompt** in natural language that could be used by an LLM to regenerate the pipeline.

It should start like:
"Generate a Kubeflow Pipeline named `XYZ` that performs..."

Be specific. Mention:
- The pipeline name
- The number of components
- The function of each component
- The inputs/outputs if visible
- The control flow (e.g., parallelFor, after, dependencies)
- Any tools/libraries used (e.g., sklearn, Snowflake)

Here is the pipeline code from `{file}`:

{code[:3000]}
"""
    try:
        response = model.generate_content(gemini_prompt)
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] Gemini failed: {str(e)}"

# Run for all pipelines
all_prompts = []
for entry in kfp_data:
    file = entry["file_path"].split("/")[-1]
    code = entry["content"]

    structured_prompt = generate_structured_prompt(code, file)
    time.sleep(1)

    all_prompts.append({
        "repo": entry["repo"],
        "file": file,
        "structured_prompt": structured_prompt
    })

# Save to JSON
with open("kfp_structured_prompts_for_llms_2.json", "w", encoding="utf-8") as f:
    json.dump(all_prompts, f, indent=2)

print("✅ Structured prompts saved to kfp_structured_prompts_for_llms.json")
