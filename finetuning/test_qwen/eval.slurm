#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --time=02:00:00
#SBATCH --job-name=kfp-eval
#SBATCH --chdir=/scratch/ilyes/kfp-gen/finetuning/test_qwen
#SBATCH --output=/scratch/ilyes/kfp-gen/finetuning/test_qwen/runs/exp1/slurm_%j.out
#SBATCH --account=def-masai45
#SBATCH --mail-user=ilkas2@ulaval.ca
#SBATCH --mail-type=ALL   

set -euo pipefail

module load python/3.11
source ~/ENV/bin/activate

# deps first time:
# pip install transformers accelerate torch kfp pylint nltk datasets

# ensure output dirs exist in the *repo*, not spool
mkdir -p runs/exp1/{gen,yaml,logs}

python ./eval.py \
  --model-path /scratch/ilyes/kfp-gen/finetuning/run/kfp-Qwen2.5-7B-Instruct/final-model \
  --hf-path /scratch/ilyes/kfp-gen/finetuning/data/prompts_dataset/test \
  --out-dir /scratch/ilyes/kfp-gen/finetuning/test_qwen/runs/exp1 \
  --max-samples 100 \
  --save-refs
