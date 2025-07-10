import os
import json
import requests
from github import Github
from tqdm import tqdm

# Load your collected repos
with open("kfp_repos.json") as f:
    repos = json.load(f)
# Load from .env file (optional but recommended)
load_dotenv()

# Access the token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw"
}

filtered_files = []
max_files_per_repo = 20  # Limit to avoid rate limits

print("Scanning repositories for @dsl.pipeline files...")

for repo_info in tqdm(repos):
    try:
        repo = g.get_repo(repo_info["full_name"])
        contents = repo.get_contents("")

        stack = contents if isinstance(contents, list) else [contents]
        checked = 0

        while stack and checked < max_files_per_repo:
            file = stack.pop(0)

            if file.type == "dir":
                stack.extend(repo.get_contents(file.path))
            elif file.name.endswith(".py"):
                raw_url = file.download_url
                r = requests.get(raw_url, headers=headers)
                if "@dsl.pipeline" in r.text or "kfp.dsl" in r.text:
                    filtered_files.append({
                        "repo": repo.full_name,
                        "file_path": file.path,
                        "raw_url": raw_url,
                        "content": r.text,
                    })
                    checked += 1
    except Exception as e:
        continue

print(f"✅ Found {len(filtered_files)} potential pipeline files.")

with open("kfp_pipeline_snippets.json", "w") as f:
    json.dump(filtered_files, f, indent=2)
