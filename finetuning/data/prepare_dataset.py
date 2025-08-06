import json
from datasets import DatasetDict, Dataset
from pathlib import Path

def construct_expected_filename(repo, file_path):
    repo_clean = repo.replace("/", "_")
    file_clean = file_path.replace("/", "_").replace("-", "_").replace(".py", "")
    return f"{repo_clean}_{file_clean}.py"

def load_raw_data():
    with open("/home/ilyes101/Documents/pfe-project/kfp-gen/finetuning/data/enhanced_prompts_structured.json") as f:
        prompts = json.load(f)

    reference_dir = Path("data/references_kfp_files")
    all_files = list(reference_dir.rglob("*.py"))
    all_file_names = {f.name: f for f in all_files}

    valid_pairs = []
    for entry in prompts:
        repo = entry.get("repo")
        file_path = entry.get("file")
        if not repo or not file_path:
            continue

        expected_filename = construct_expected_filename(repo, file_path)
        matched_file = all_file_names.get(expected_filename)

        if matched_file and matched_file.exists():
            code = matched_file.read_text()
            valid_pairs.append({
                "prompt": entry["enhanced_prompt"],
                "completion": code
            })
        else:
            print(f"⚠️ No match found for: {expected_filename}")

    return valid_pairs

if __name__ == "__main__":
    data = load_raw_data()
    if not data:
        raise RuntimeError("❌ No valid data found. Please verify the filename matching logic.")

    split_index = int(0.9 * len(data))
    train_split = data[:split_index]
    test_split = data[split_index:]

    dataset = DatasetDict({
        "train": Dataset.from_list(train_split),
        "test": Dataset.from_list(test_split)
    })

    dataset.save_to_disk("data/prompts_dataset")
    print(f"✅ Saved dataset with {len(train_split)} train and {len(test_split)} test examples.")
