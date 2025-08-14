#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100l:1
#SBATCH --mem=30000
#SBATCH --cpus-per-task=16
#SBATCH --time=10:00:00
#SBATCH --job-name=kfp-qwen-sft
#SBATCH --output=logs/kfp_qwen_sft_%j.out
#SBATCH --account=def-masai45
#SBATCH --mail-user=ilkas2@ulaval.ca
#SBATCH --mail-type=ALL

# --- Modules & env ---
module --force purge
module load StdEnv/2023
module load python/3.11
# (PyTorch in your venv already includes CUDA libs; no need for nvcc)

source ~/ENV/bin/activate

# Nice-to-have env (helps allocator & keeps logs clean)
export TOKENIZERS_PARALLELISM=false
# combine both allocator tweaks:
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,max_split_size_mb:256

# Navigate to project directory
cd /home/ilyes/scratch/kfp-gen/finetuning

# Keep one visible GPU (optional on single-GPU job)
export CUDA_VISIBLE_DEVICES=0

# Run fine-tuning script
python unsloth_trainer/train_sft.py \
  --model /scratch/ilyes/models/Qwen/Qwen2.5-7B-Instruct \
  --dataset /home/ilyes/scratch/kfp-gen/finetuning/data/data/prompts_dataset \
  --run_name "kfp-Qwen2.5-7B-Instruct" \
  --output_dir "run/kfp-Qwen2.5-7B-Instruct" \
  --batch 1 \
  --grad 8 \
  --context 1024
