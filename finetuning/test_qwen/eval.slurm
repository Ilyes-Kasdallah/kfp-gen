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
module load arrow                 # <-- important (pyarrow provided here)

source ~/ENV/bin/activate
python -m pip install --upgrade pip
python -m pip install "transformers==4.40.2" "accelerate>=0.29" "tokenizers<0.20" \
                      "torch" "numpy>=1.26.4" "nltk>=3.8" "pylint>=3.0" "kfp>=2.5"

export PATH="$HOME/bin:$PATH"     # if kube-linter is in ~/bin

cd /scratch/ilyes/kfp-gen/finetuning/test_qwen
python ./eval.py \
  --model-path /scratch/ilyes/kfp-gen/finetuning/run/kfp-Qwen2.5-7B-Instruct/final-model \
  --hf-path     /scratch/ilyes/kfp-gen/finetuning/data/prompts_dataset \
  --out-dir     /scratch/ilyes/kfp-gen/finetuning/testing_qwen/runs/exp1 \
  --max-samples 50 \
  --save-refs
