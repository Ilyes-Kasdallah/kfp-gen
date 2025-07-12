# 🧠 KFP-GEN: Kubeflow Pipeline Generation and Evaluation

A Python + Jupyter project for collecting, generating, and evaluating Kubeflow Pipelines (KFP) using Large Language Models (LLMs). The current setup focuses on testing `Qwen2.5-Coder-1.5B-Instruct` in Google Colab using prompts generated from real-world KFP pipelines. The next step involves evaluating the similarity between the generated pipelines and their reference implementations.

---

## 📁 Repository Structure

kfp-gen/
├── data_collect/ # Scripts and notebooks for pipeline data collection
├── testing-llms/ # Scripts and notebooks for LLM prompt execution and evaluation
├── .gitignore # Ignore rules for Git
└── README.md # Project documentation


---

## 🔹 `data_collect/`

Contains Python scripts and Jupyter notebooks to automate the process of gathering Kubeflow pipeline examples from GitHub and preparing prompts. Tasks include:

- Connecting to data sources (e.g., GitHub API)
- Extracting KFP-related YAML/Python files
- Generating structured prompts from real pipelines
- Preprocessing and storing references for evaluation

---

## 🔹 `testing-llms/`

Includes scripts and tools for testing and evaluating LLMs such as Qwen2.5:

- Running generated prompts through Qwen2.5 using Colab
- Generating Kubeflow pipelines in Python using KFP v2 DSL
- Saving generated outputs for evaluation
- Next phase: measuring similarity between generated and reference code (e.g., BLEU score)

---

## 🔹 `.gitignore`

A standard ignore file to exclude:

- Compiled Python files (`.pyc`)
- Jupyter notebook checkpoints
- Environment folders
- Temporary output files

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ilyes-Kasdallah/kfp-gen.git
cd kfp-gen

2. Install dependencies

Requirements:

    Python 3.8+
    kfp (Kubeflow Pipelines SDK)
    transformers, huggingface_hub (for LLMs)

3. Explore directories

    data_collect/: for prompt generation and pipeline scraping

    testing-llms/: for interacting with LLMs and evaluating generated code

Summary Table

| Item            | Description                                                      |
| --------------- | ---------------------------------------------------------------- |
| `data_collect/` | Contains scripts/notebooks to fetch and preprocess KFP pipelines |
| `testing-llms/` | Hosts prompt experiments and LLM output generation/evaluation    |
| `.gitignore`    | Excludes generated, temporary, and environment files             |
