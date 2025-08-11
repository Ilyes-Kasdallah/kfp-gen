#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --time=02:00:00
#SBATCH --job-name=kfp-eval
#SBATCH --output=testing_qwen/runs/exp1/slurm_%j.out
#SBATCH --account=def-masai45

module load python/3.11
source ~/ENV/bin/activate
cd $SLURM_SUBMIT_DIR

# First time only:
# pip install transformers accelerate torch kfp pylint nltk datasets

# Make sure kube-linter is in PATH on the node (e.g., /usr/local/bin/kube-linter)

python finetuning/testing_qwen/eval.py \
  --model-path /home/ilyes/scratch/kfp-gen/finetuning/run/kfp-Qwen2.5-7B-Instruct\final-model \
  --hf-path finetuning/data/prompts_dataset/test \
  --out-dir finetuning/testing_qwen/runs/exp1 \
  --max-samples 100 \
  --save-refs
