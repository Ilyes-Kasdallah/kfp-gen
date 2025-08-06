#!/bin/bash
module load python/3.11
source ~/ENV/bin/activate

cd /home/ilyes/scratch/kfp-gen/finetuning
pip install -r requirements.txt

#python data/prepare_dataset.py

python unsloth_trainer/train_sft.py \
  --model Qwen/Qwen1.5-8B \
  --dataset data/prompts_dataset \
  --rname "kfp-qwen3b" \
  --output "run/kfp-qwen3b" \
  --batch 1 \
  --grad 4 \
  --context 2048
