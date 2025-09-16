
# KFP-GEN — Kubeflow Pipeline Generation, Fine-Tuning & Evaluation

KFP-GEN is our end-to-end toolkit to **collect** real Kubeflow Pipelines (KFP), **fine-tune** large language models to generate KFP v2 DSL code, and **evaluate** the generations against reference implementations.

* **Models:** Qwen-series (e.g., `Qwen/Qwen2.5-7B-Instruct`) fine-tuned with Unsloth LoRA SFT
* **Targets:** Kubeflow Pipelines v2 (Python DSL)
* **Environment:** HPC clusters (Compute Canada style, Slurm), offline wheels, V100 GPUs
* **Core scripts:**

  * `finetuning/init.sh` → set up our environment, install packages, optionally download a model and clone a dataset
  * `finetuning/traintest.sh` → Slurm job to fine-tune with Unsloth + BitsAndBytes

---

## Repository Structure

```
kfp-gen/
├─ data_collect/       # Scripts and notebooks to collect KFP examples and build prompts
├─ generate-kfp/       # Tools to prompt models and generate KFP v2 DSL code
├─ testing-llms/       # Compilation tests and similarity evaluation
├─ finetuning/
│  ├─ init.sh          # HPC bootstrap script
│  ├─ traintest.sh     # Slurm job for supervised fine-tuning
│  ├─ requirements.txt # Offline wheel requirements
│  └─ unsloth_trainer/
│     └─ train_sft.py  # Training entrypoint
└─ README.md
```

---

## Quick Start (HPC / Slurm)

### 1) Initialize environment, model, and dataset

```bash
cd finetuning
# Usage: sh ./init.sh <huggingface-model-id> <git-dataset-url>
# Example:
sh ./init.sh Qwen/Qwen2.5-7B-Instruct https://github.com/logpai/loghub.git
```

What `init.sh` does for us:

1. Loads modules (defined in `statics/modules.sh`)
2. Creates a virtualenv at `$HOME/ENV`
3. Installs Python packages offline using `requirements.txt`
4. Optionally downloads a Hugging Face model into `$SCRATCH/models/<MODEL_ID>`
5. Optionally clones a dataset repo into `$SCRATCH/dataset/<name>`

At the end, it prints the paths to our environment, model, and dataset.

---

### 2) Prepare Python 3.11 venv (if not done by init)

Our training script (`traintest.sh`) assumes Python 3.11. On the cluster:

```bash
module --force purge
module load StdEnv/2023 gcc/12.3 python/3.11 arrow
python -m venv ~/ENV311
source ~/ENV311/bin/activate
pip install --no-index --upgrade pip
pip install --no-index -r /home/$USER/scratch/kfp-gen/finetuning/requirements.txt
```

---

### 3) Submit fine-tuning job

We submit the training script as a Slurm job:

```bash
cd finetuning
sbatch traintest.sh
```

`traintest.sh` requests:

* **1x V100 GPU**, 30 GB RAM, 16 CPUs, 10h walltime
* Loads Python 3.11 environment
* Validates BitsAndBytes CUDA libraries
* Runs:

```bash
python unsloth_trainer/train_sft.py \
  --model /scratch/$USER/models/Qwen/Qwen2.5-7B-Instruct \
  --dataset /home/$USER/scratch/kfp-gen/finetuning/data/data/prompts_dataset \
  --run_name "kfp-Qwen2.5-7B-Instruct" \
  --output_dir "run/kfp-Qwen2.5-7B-Instruct" \
  --batch 1 \
  --grad 8 \
  --context 2048
```

Logs are written under `logs/kfp_qwen_sft_%j.out`.

---

## Dataset Format

Our fine-tuning dataset should contain **prompt → KFP code** pairs. We recommend a JSONL format:

```json
{"input": "<structured prompt describing pipeline>", "output": "<kfp v2 DSL code>"}
```

Suggested structure:

```
finetuning/
└─ data/
   └─ data/
      └─ prompts_dataset/
         ├─ train.jsonl
         ├─ val.jsonl
         └─ test.jsonl
```

---

## Generation & Evaluation

After training, we:

1. **Generate** new KFP pipelines with our model (using `generate-kfp/`).
2. **Check validity** by compiling pipelines (`compiler.Compiler().compile(...)`).
3. **Evaluate similarity**:

   * Textual metrics: BLEU, METEOR
   * Structural metrics (planned): DAG/AST comparison (components, edges, parameters)
4. **Report results** in `outputs/eval/`.

---

## Configuration

We can avoid hard-coded paths with a config YAML:

```yaml
paths:
  dataset: /home/$USER/scratch/kfp-gen/finetuning/data/data/prompts_dataset
  model_root: /scratch/$USER/models
  outputs: /scratch/$USER/kfp-gen/finetuning/run

train:
  model_id: Qwen/Qwen2.5-7B-Instruct
  batch: 1
  grad_accum: 8
  context: 2048
  run_name: kfp-Qwen2.5-7B-Instruct
```


## Citation

```
Kasdallah, I. (2025). KFP-GEN: Kubeflow Pipeline Generation, Fine-Tuning & Evaluation.
GitHub: https://github.com/Ilyes-Kasdallah/kfp-gen
```

