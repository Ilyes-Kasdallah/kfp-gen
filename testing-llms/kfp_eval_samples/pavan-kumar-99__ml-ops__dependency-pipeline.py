```python
from kfp import dsl
from kfp.components import load_component_from_text

# Load the echo component
echo_op = load_component_from_text("""
name: Echo
description: A simple echo component.
inputs:
- {type: STRING, description: Input string}
outputs:
- {type: STRING, description: Output string}
implementation:
  container:
    image: alpine
    command: ["sh", "-c", "echo $INPUT"]
""")

# Load the printString component
print_string_op = load_component_from_text("""
name: Print String
description: A custom component that prints a string.
inputs:
- {type: STRING, description: Input string}
outputs:
- {}
implementation:
  container:
    image: alpine
    command: ["sh", "-c", "echo $INPUT"]
""")

# Define the pipeline
@dsl.pipeline(name="dependency-pipeline")
def dependency_pipeline():
    # Step 1: Execute the echo component
    step1 = echo_op(input="Hi Kubeflow")
    
    # Step 2: Execute the printString component after step1
    step2 = print_string_op(input=step1.output)

# Compile the pipeline
pipeline_spec = dsl.compiler.Compiler().compile(dependency_pipeline, package_path='dependency-pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `dependency-pipeline` that includes two components: `echo` and `printString`. The `echo` component uses the `alpine` image and executes a shell command to print "Hi Kubeflow". The `printString` component takes a string as input and prints it to standard output. The pipeline's control flow is sequential, with the `printString` component running after the `echo` component completes. The pipeline is compiled into a YAML file named `dependency-pipeline.yaml`, which can be deployed on a Kubernetes cluster using Kubeflow Pipelines.