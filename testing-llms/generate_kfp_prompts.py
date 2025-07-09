import json
import re
import requests
from pathlib import Path

# ---- Configuration ----
INPUT_FILE = "kfp_pipeline_snippets.json"   #  dataset
OUTPUT_DIR = Path("kfp_eval_samples")       # Output folder
OUTPUT_DIR.mkdir(exist_ok=True)

# ---- Helper Functions ----
def fetch_readme(repo_url):
    """Fetch README.md from GitHub repo using 'main' or 'master'."""
    if "github.com" not in repo_url:
        return None
    try:
        repo_path = repo_url.replace("https://github.com/", "").strip("/")
        for branch in ["main", "master"]:
            raw_url = f"https://raw.githubusercontent.com/{repo_path}/{branch}/README.md"
            response = requests.get(raw_url)
            if response.status_code == 200:
                return response.text
    except Exception:
        return None
    return None

def extract_high_quality_summary(readme):
    """Get meaningful description from README's overview or usage section."""
    if not readme:
        return None
    lines = readme.splitlines()
    content = []
    inside = False
    for line in lines:
        if re.match(r"#+\s*(overview|description|pipeline|usage|introduction)", line, re.IGNORECASE):
            inside = True
            continue
        if inside:
            if line.strip() == "" or line.strip().startswith("#"):
                break
            content.append(line.strip())
    return " ".join(content).strip() if content else None

def extract_docstring_and_comments(code):
    """Fallback to extracting docstring and top comments from code."""
    docstring = re.search(r'"""(.*?)"""', code, re.DOTALL)
    doc = docstring.group(1).strip().replace('\n', ' ') if docstring else ""
    comments = [line.strip("#").strip() for line in code.splitlines() if line.strip().startswith("#")]
    return f"{doc} {' '.join(comments[:5])}".strip()

# ---- Main Execution ----
def main():
    with open(INPUT_FILE) as f:
        kfp_data = json.load(f)

    results = []

    for i, entry in enumerate(kfp_data, 1):
        repo_url = entry.get("repo", "")
        file_path = entry.get("file_path", "")
        code = entry.get("content", "")

        readme = fetch_readme(repo_url)
        summary = extract_high_quality_summary(readme)
        fallback = extract_docstring_and_comments(code)

        if summary:
            prompt = f"You are an MLOps engineer. Write a complete Kubeflow pipeline based on the project context:\n\n{summary}"
        elif fallback:
            prompt = f"You are an MLOps engineer. Write a Kubeflow pipeline based on the following description and code logic:\n\n{fallback}"
        else:
            prompt = "Design a Kubeflow pipeline that matches the logic of this Python code snippet."

        # Save prompt and reference
        (OUTPUT_DIR / f"sample_{i}_prompt.txt").write_text(prompt)
        (OUTPUT_DIR / f"sample_{i}_reference.py").write_text(code)

        results.append({
            "id": i,
            "repo": repo_url,
            "file_path": file_path,
            "prompt": prompt
        })

    # Save metadata
    with open(OUTPUT_DIR / "prompt_metadata_full.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ {len(results)} prompts saved to '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    main()
