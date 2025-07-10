import os
import json
import requests
from github import Github
from tqdm import tqdm

# Configuration
load_dotenv()

# Access the token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Replace with your GitHub token
REPOS_FILE = "kfp_repos.json"
OUTPUT_JSON = "kfp_pipeline_snippets.json"
OUTPUT_DIR = "kfp_pipeline_files"
MAX_FILES_PER_REPO = 500

# Authenticate GitHub API
g = Github(GITHUB_TOKEN)
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw"
}

# Load collected repo metadata
with open(REPOS_FILE) as f:
    repos = json.load(f)

filtered_files = []
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🔍 Scanning repositories for Kubeflow pipeline files...")

for repo_info in tqdm(repos):
    try:
        repo = g.get_repo(repo_info["full_name"])
        contents = repo.get_contents("")
        stack = contents if isinstance(contents, list) else [contents]
        checked = 0

        while stack and checked < MAX_FILES_PER_REPO:
            file = stack.pop(0)

            if file.type == "dir":
                stack.extend(repo.get_contents(file.path))
            elif file.name.endswith(".py"):
                raw_url = file.download_url
                r = requests.get(raw_url, headers=headers)
                if r.status_code == 200 and ("@dsl.pipeline" in r.text or "kfp.dsl" in r.text):
                    item = {
                        "repo": repo.full_name,
                        "file_path": file.path,
                        "raw_url": raw_url,
                        "content": r.text,
                    }
                    filtered_files.append(item)

                    # Save locally as .py file
                    filename = f'{repo.full_name.replace("/", "__")}__{os.path.basename(file.path)}'
                    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f_out:
                        f_out.write(r.text)

                    checked += 1

    except Exception as e:
        continue

# Save metadata and content to JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(filtered_files, f, indent=2)

print(f"\n✅ Done! {len(filtered_files)} pipeline files saved to '{OUTPUT_DIR}/' and metadata to '{OUTPUT_JSON}'.")
