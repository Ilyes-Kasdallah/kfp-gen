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

module --force purge
module load StdEnv/2023 gcc/12.3 python/3.11 arrow

source ~/ENV311/bin/activate

# Make sure Torch’s CUDA libs are visible
TORCH_LIB_DIR="$(python - <<'PY'
import os, torch
print(os.path.join(os.path.dirname(torch.__file__), "lib"))
PY
)"
export LD_LIBRARY_PATH="${TORCH_LIB_DIR}:${LD_LIBRARY_PATH:-}"

# IMPORTANT: don't force a non-existent CUDA variant
unset BNB_CUDA_VERSION

# Sanity check: bnb + CUDA
python - <<'PY'
import sys, torch, bitsandbytes, glob, pathlib
print("Node Python:", sys.version.split()[0])
print("Torch CUDA:", torch.version.cuda, "Devices:", torch.cuda.device_count())
p = pathlib.Path(bitsandbytes.__file__).parent
libs = sorted(glob.glob(str(p/'libbitsandbytes_cuda*.so')))
print("bnb libs:", [pathlib.Path(x).name for x in libs])
import bitsandbytes as bnb
print("bitsandbytes:", bnb.__version__, "OK")
PY

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,max_split_size_mb:256
export CUDA_VISIBLE_DEVICES=0

cd /scratch/ilyes/kfp-gen/finetuning

python unsloth_trainer/train_sft.py \
  --model /scratch/ilyes/models/Qwen/Qwen2.5-7B-Instruct \
  --dataset /home/ilyes/scratch/kfp-gen/finetuning/data/data/prompts_dataset \
  --run_name "kfp-Qwen2.5-7B-Instruct" \
  --output_dir "run/kfp-Qwen2.5-7B-Instruct" \
  --batch 1 \
  --grad 8 \
  --context 2048
