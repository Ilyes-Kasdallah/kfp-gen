#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --time=02:00:00
#SBATCH --job-name=kfp-eval
#SBATCH --chdir=/scratch/ilyes/kfp-gen/finetuning/test_qwen
#SBATCH --output=/scratch/ilyes/kfp-gen/finetuning/test_qwen/runs/slurm_%j.out
#SBATCH --account=def-masai45
#SBATCH --mail-user=ilkas2@ulaval.ca
#SBATCH --mail-type=ALL

module purge
module load StdEnv/2023
module load python/3.12
module load arrow                 # provides pyarrow on Compute Canada

source ~/ENV/bin/activate
python -m pip install --upgrade pip setuptools wheel

# Start clean to avoid solver dead-ends
python -m pip uninstall -y wandb protobuf tokenizers transformers kfp || true

# 1) Core stack (wheel-only; no Rust build). We stay on transformers 4.40.2 + tokenizers 0.19.1,
#    and rely on the slow-tokenizer fallback in eval.py to avoid the fast Rust tokenizer.
PIP_ONLY_BINARY=:all: python -m pip install \
  "transformers==4.40.2" \
  "tokenizers==0.19.1" \
  "accelerate>=0.29" \
  "torch" \
  "numpy>=1.26.4,<2" \
  "nltk>=3.8" \
  "pylint>=3.0" \
  "datasets>=2.18,<3"

# 2) kfp requires protobuf==6.31.1; install them together so the resolver is happy
PIP_ONLY_BINARY=:all: python -m pip install \
  "protobuf==6.31.1" \
  "kfp==2.14.2"

# (Optional) If you truly need W&B in this job, try a version compatible with protobuf 6.
# Otherwise, keep it uninstalled for this eval job to avoid conflicts.
# python -m pip install "wandb>=0.19" || true

# Quick sanity print
python - <<'PY'
try:
    import transformers, tokenizers
    import google.protobuf as pb
    import kfp
    print("transformers:", transformers.__version__)
    print("tokenizers  :", tokenizers.__version__)
    print("protobuf    :", pb.__version__)
    print("kfp         :", kfp.__version__)
except Exception as e:
    print("Sanity import failed:", e)
PY

cd /scratch/ilyes/kfp-gen/finetuning/test_qwen
python ./eval.py \
  --model-path /scratch/ilyes/kfp-gen/finetuning/run/kfp-Qwen2.5-7B-Instruct/final-model \
  --hf-path     /scratch/ilyes/kfp-gen/finetuning/data/prompts_dataset \
  --out-dir     /scratch/ilyes/kfp-gen/finetuning/testing_qwen/runs/exp1 \
  --max-samples 50 \
  --save-refs
