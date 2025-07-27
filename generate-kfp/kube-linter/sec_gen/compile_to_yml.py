import os
import traceback
from pathlib import Path
from kfp.compiler import Compiler
from importlib.util import spec_from_file_location, module_from_spec

base_dir = Path("/home/ilyes101/Documents/pfe-project/kfp-gen/generate-kfp/kube-linter/sec_gen/kfp_eval_samples_enhanced")
output_dir = Path("compiled_yaml_outputs")
output_dir.mkdir(exist_ok=True)

report = []

for py_file in base_dir.glob("*.py"):
    try:
        module_name = py_file.stem.replace("-", "_")
        spec = spec_from_file_location(module_name, py_file)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)

        pipeline_func = None
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if callable(obj) and hasattr(obj, "_component_hints"):
                pipeline_func = obj
                break

        if pipeline_func is None:
            raise ValueError("No pipeline function found.")

        yaml_path = output_dir / f"{py_file.stem}.yaml"
        Compiler().compile(pipeline_func, package_path=yaml_path)
        report.append((py_file.name, "✅ Success"))

    except Exception as e:
        report.append((py_file.name, f"❌ {type(e).__name__}: {str(e).strip().splitlines()[0]}"))

# Save report
import pandas as pd
df = pd.DataFrame(report, columns=["File", "Status"])
df.to_csv("kfp_compilation_report.csv", index=False)
print("✅ Compilation report saved as kfp_compilation_report.csv")
