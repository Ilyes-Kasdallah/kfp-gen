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
module load arrow                 # provides pyarrow on Compute Canada

source ~/ENV/bin/activate
python -m pip install --upgrade pip setuptools wheel

# Avoid TRL forcing newer transformers if it’s present (not needed for eval)
python -m pip uninstall -y trl || true

# Force wheels only (prebuilt in CC wheelhouse), avoid building Rust tokenizers
# Pin versions compatible with slow tokenizer fallback (no need for tokenizers>=0.20)
PIP_ONLY_BINARY=:all: python -m pip install \
  "protobuf>=5.29,<6" \
  "transformers==4.40.2" \
  "tokenizers==0.19.1" \
  "accelerate>=0.29" \
  "torch" \
  "numpy>=1.26.4,<2" \
  "nltk>=3.8" \
  "pylint>=3.0" \
  "datasets>=2.18,<3" \
  "kfp>=2.5"

# Sanity print
python - <<'PY'
import transformers, tokenizers
import google.protobuf as pb
print("transformers:", transformers.__version__)
print("tokenizers  :", tokenizers.__version__)
print("protobuf    :", pb.__version__)
PY

# Prefer slow tokenizers to avoid Rust completely
export TRANSFORMERS_NO_FAST_TOKENIZER=1
export PATH="$HOME/bin:$PATH"     # if kube-linter is in ~/bin

cd /scratch/ilyes/kfp-gen/finetuning/test_qwen
python ./eval.py \
  --model-path /scratch/ilyes/kfp-gen/finetuning/run/kfp-Qwen2.5-7B-Instruct/final-model \
  --hf-path     /scratch/ilyes/kfp-gen/finetuning/data/prompts_dataset \
  --out-dir     /scratch/ilyes/kfp-gen/finetuning/testing_qwen/runs/exp1 \
  --max-samples 50 \
  --save-refs
