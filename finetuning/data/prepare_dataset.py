import json
from datasets import DatasetDict, Dataset
from pathlib import Path

# Load filtered prompts
with open("/home/ilyes101/Documents/pfe-project/kfp-gen/finetuning/data/references_prompts.json") as f:
    prompts = json.load(f)

# Index .py files in folder
reference_dir = Path("/home/ilyes101/Documents/pfe-project/kfp-gen/finetuning/data/references_kfp_files")
all_files = {f.name: f for f in reference_dir.rglob("*.py")}

valid_pairs = []
for entry in prompts:
    file_name = entry.get("file")
    prompt = entry.get("structured_prompt")

    if not file_name or not prompt:
        continue

    matched_file = all_files.get(Path(file_name).name)
    if matched_file:
        code = matched_file.read_text()
        valid_pairs.append({
            "prompt": prompt.strip(),
            "completion": code.strip()
        })
    else:
        print(f"⚠️ No match found for: {file_name}")

# Exit if empty
if not valid_pairs:
    raise RuntimeError("❌ No valid data matched. Check folder and prompt paths.")

# Split 90/10
split_index = int(0.9 * len(valid_pairs))
train_split = valid_pairs[:split_index]
test_split = valid_pairs[split_index:]

# Save as HuggingFace Dataset
dataset = DatasetDict({
    "train": Dataset.from_list(train_split),
    "test": Dataset.from_list(test_split)
})
dataset.save_to_disk("data/prompts_dataset")
print(f"✅ HuggingFace dataset saved with {len(train_split)} train / {len(test_split)} test")

# Also save as .jsonl
with open("data/prompts_dataset_train.jsonl", "w", encoding="utf-8") as f:
    for item in train_split:
        json.dump(item, f)
        f.write("\n")
print("✅ prompts_dataset_train.jsonl saved")
