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


module load python/3.12  # or your usual module
source ~/ENV/bin/activate
python -m pip install --upgrade pip

# Choose ONE of the lines below (A or B)

python -m pip install "transformers==4.40.2" "accelerate>=0.29" "tokenizers<0.20" \
                      "torch" "numpy>=1.26.4" "datasets>=2.19" "nltk>=3.8" "pylint>=3.0" "kfp>=2.5"

# python -m pip install "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2" \
#                       "transformers>=4.41" "accelerate>=0.29" "datasets>=2.19" \
#                       "nltk>=3.8" "pylint>=3.0" "kfp>=2.5" "torch"

# (optional) kube-linter binary: put it in ~/bin and ensure PATH has it
export PATH="$HOME/bin:$PATH"

# Run evaluation
cd /scratch/ilyes/kfp-gen/finetuning/test_qwen
python ./eval.py \
  --model-path <your-finetuned-model-or-HF-id> \
  --hf-path /scratch/ilyes/kfp-gen/finetuning/data/prompts_dataset \
  --out-dir /scratch/ilyes/kfp-gen/finetuning/testing_qwen/runs/exp1 \
  --max_samples 50 \
  --save-refs
