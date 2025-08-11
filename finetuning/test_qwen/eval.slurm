#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --time=02:00:00
#SBATCH --job-name=kfp-eval
#SBATCH --output=./runs/exp1/slurm_%j.out
#SBATCH --account=def-masai45
#SBATCH --mail-user=ilkas2@ulaval.ca
#SBATCH --mail-type=ALL 

set -euo pipefail

module load python/3.11
source ~/ENV/bin/activate

# Always run from the directory where this script lives
cd "$(dirname "$0")"
echo "PWD = $(pwd)"

# One-time, if needed:
# pip install transformers accelerate torch kfp pylint nltk datasets

# Ensure kube-linter is in PATH (e.g., /usr/local/bin/kube-linter)
mkdir -p runs/exp1/{gen,yaml,logs}

python ./eval.py \
  --model-path ../run/kfp-Qwen2.5-7B-Instruct/final-model \
  --hf-path ../data/prompts_dataset/test \
  --out-dir ./runs/exp1 \
  --max-samples 100 \
  --save-refs
