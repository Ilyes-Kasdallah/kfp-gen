import subprocess
def pylint_score(code):
    with open("temp.py", "w") as f: f.write(code)
    result = subprocess.run(["pylint", "temp.py", "--disable=all", "--enable=syntax-error"], capture_output=True, text=True)
    return 10.0 if result.returncode == 0 else 0.0
