# Leave any active venv
deactivate 2>/dev/null || true

# Clean stack and load CC modules (Arrow BEFORE venv)
module purge
module load StdEnv/2023 gcc/12.3 python/3.11 arrow

# Sanity check
python -V   # should be 3.11.x

# New venv (keep old one around if you want)
python -m venv ~/ENV311
source ~/ENV311/bin/activate
pip install --upgrade pip wheel setuptools

# Install your requirements (pyarrow will be provided by the module)
pip install --no-cache-dir -r /scratch/ilyes/kfp-gen/finetuning/requirements.txt

# Quick check
python - <<'PY'
import sys
print("Python:", sys.version)
import pyarrow as pa
print("pyarrow:", pa.__version__)
PY
