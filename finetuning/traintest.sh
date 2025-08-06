#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1           # Request 4 V100 GPUs
#SBATCH --mem=30000                 # More RAM for big batches/context
#SBATCH --cpus-per-task=16           # Use more CPUs for dataloader
#SBATCH --time=01:00:00                  # Max time (hh:mm:ss)
#SBATCH --job-name=kfp-qwen-sft
#SBATCH --output=logs/kfp_qwen_sft_%j.out
#SBATCH --account=def-masai45  
#SBATCH --mail-user=ilkas2@ulaval.ca
#SBATCH --mail-type=ALL   

# Load modules and activate environment
module load python/3.11
source ~/ENV/bin/activate

# Navigate to working directory
cd /home/ilyes/scratch/kfp-gen/finetuning

# (Optional) Install requirements if not done already
# pip install -r requirements.txt

# Run fine-tuning
python unsloth_trainer/train_sft.py \
  --model Qwen/Qwen1.5-1.8B \
  --dataset data/prompts_dataset \
  --rname "kfp-qwen1.8b" \
  --output "run/kfp-qwen1.8b" \
  --batch 1 \
  --grad 4 \
  --context 2048
