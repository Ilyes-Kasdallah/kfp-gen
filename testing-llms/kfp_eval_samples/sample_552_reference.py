import sys
import os
import ast
import re
from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Model

def read_python_file(file_path):
    """ Reads the content of the given Python file. """
    with open(file_path, "r") as f:
        return f.read()

def extract_functions(code):
    """ Extracts function definitions from Python code. """
    tree = ast.parse(code)
    functions = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            function_body = "\n".join([ast.unparse(stmt) for stmt in node.body])
            if function_body.strip():
                args = [arg.arg for arg in node.args.args]
                num_outputs = function_body.count("return ")

                functions[node.name] = {
                    "body": function_body,
                    "args": args,
                    "num_outputs": num_outputs
                }

    return functions

def extract_imports(code):
    """ Extracts all import statements from Python code. """
    tree = ast.parse(code)
    imports = []

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))

    return "\n".join(imports)

def convert_to_kfp_dsl(file_path):
    """ Converts a given Python ML script into a Kubeflow Pipelines DSL format. """
    code = read_python_file(file_path)
    functions = extract_functions(code)
    imports = extract_imports(code)

    if not functions:
        print("No functions found in the provided script.")
        sys.exit(1)

    dsl_code = """
from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Model
""" + imports + "\n"

    component_templates = []
    function_calls = []
    previous_outputs = {}

    for function_name, details in functions.items():
        function_body = details["body"]
        function_args = details["args"]
        num_outputs = details["num_outputs"]

        kfp_args = ", ".join([f"{arg}: Dataset" for arg in function_args])

        # Fix: Handling multiple outputs correctly
        if function_name == "preprocess_data":
            return_type = "Tuple[Dataset, Dataset]"
            output_vars = ["X_train", "y_train"]
        elif function_name == "train_model":
            return_type = "Model"
            output_vars = ["model"]
        elif function_name == "load_data":
            return_type = "Dataset"
            output_vars = ["df"]
        else:
            return_type = "Dataset"
            output_vars = ["output"]

        outputs = ", ".join(output_vars)

        component_templates.append(f"""
@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn", "tensorflow"]
)
def {function_name}({kfp_args}) -> {return_type}:
{re.sub("^", "    ", function_body, flags=re.MULTILINE)}
""")

        # Store outputs with correct variable names
        if function_args:
            input_args = []
            for arg in function_args:
                if arg in previous_outputs:
                    input_args.append(f"{previous_outputs[arg]}.output")
                else:
                    print(f"⚠️ Warning: Argument '{arg}' not found in previous outputs!")
                    input_args.append("MISSING_ARG")

            input_args_str = ", ".join(input_args)
            function_calls.append(f"    {outputs} = {function_name}({input_args_str})")
        else:
            function_calls.append(f"    {outputs} = {function_name}()")

        print(f"🔹 Storing function output: {function_name} -> {outputs}")

        # Fix: Store multiple outputs correctly
        for i, arg in enumerate(output_vars):
            previous_outputs[arg] = output_vars[i]

    dsl_code += "\n".join(component_templates) + "\n"

    dsl_code += """
@dsl.pipeline(name="ml-pipeline")
def ml_pipeline():
""" + "\n".join(function_calls) + "\n"

    dsl_code += """
if __name__ == "__main__":
    from kfp import compiler
    compiler.Compiler().compile(ml_pipeline, "ml_pipeline.yaml")
"""

    return dsl_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dsl-convert.py <input_python_script>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        sys.exit(1)

    dsl_output = convert_to_kfp_dsl(input_file)

    output_file = "generated_new_pipeline.py"
    with open(output_file, "w") as f:
        f.write(dsl_output)

    print(f"✅ Successfully generated Kubeflow DSL: {output_file}")
