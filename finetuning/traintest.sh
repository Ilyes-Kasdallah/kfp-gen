#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1
#SBATCH --mem=30G
#SBATCH --cpus-per-task=16
#SBATCH --time=10:00:00
#SBATCH --job-name=kfp-qwen-sft
#SBATCH --output=logs/kfp_qwen_sft_%j.out
#SBATCH --account=def-masai45
#SBATCH --mail-user=ilkas2@ulaval.ca
#SBATCH --mail-type=ALL

set -euo pipefail

# --- Modules FIRST (arrow before venv) ---
module --force purge
module load StdEnv/2023 gcc/12.3 python/3.11 arrow

# Quick check on the compute node
python - <<'PY'
import sys
print("Node Python:", sys.version.split()[0])
try:
    import pyarrow as pa
    print("pyarrow OK:", pa.__version__)
except Exception as e:
    print("pyarrow import failed:", e)
    raise SystemExit(1)
PY

# --- Then activate the Py3.11 venv ---
source ~/ENV311/bin/activate

# Optional runtime knobs
export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,max_split_size_mb:256
export CUDA_VISIBLE_DEVICES=0

# Work from fast scratch (adjust if your data is elsewhere)
cd /scratch/ilyes/kfp-gen/finetuning

# Run fine-tuning
python unsloth_trainer/train_sft.py \
  --model /scratch/ilyes/models/Qwen/Qwen2.5-7B-Instruct \
  --dataset /home/ilyes/scratch/kfp-gen/finetuning/data/data/prompts_dataset \
  --run_name "kfp-Qwen2.5-7B-Instruct" \
  --output_dir "run/kfp-Qwen2.5-7B-Instruct" \
  --batch 1 \
  --grad 8 \
  --context 1536
