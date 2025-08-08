#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1           # Request 4 V100 GPUs
#SBATCH --mem=30000                 # More RAM for big batches/context
#SBATCH --cpus-per-task=16           # Use more CPUs for dataloader
#SBATCH --time=10:00:00                  # Max time (hh:mm:ss)
#SBATCH --job-name=kfp-qwen-sft
#SBATCH --output=logs/kfp_qwen_sft_%j.out
#SBATCH --account=def-masai45  
#SBATCH --mail-user=ilkas2@ulaval.ca
#SBATCH --mail-type=ALL   

# Load modules and activate environment
module load python/3.11
source ~/ENV/bin/activate

# Navigate to project directory
cd /home/ilyes/scratch/kfp-gen/finetuning

# Configure CUDA
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128

# Run fine-tuning script
python unsloth_trainer/train_sft.py \
  --model /scratch/ilyes/models/Qwen/Qwen2.5-7B-Instruct \
  --dataset /home/ilyes/scratch/kfp-gen/finetuning/data/data/prompts_dataset \
  --run_name "kfp-Qwen2.5-7B-Instruct" \
  --output_dir "run/kfp-Qwen2.5-7B-Instruct" \
  --batch 1 \
  --grad 4 \
  --context 2048

