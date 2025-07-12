```python
import kfp
from kfp import dsl

# Define the print_message component
@dsl.component(
    base_image="ubuntu",
    packages_to_install=["pip"],
    outputs={"output": dsl.OutputArtifact("text")}
)
def print_message(message: str) -> str:
    # Print the message
    print(message)
    return message

# Define the test_pipeline
@test_pipeline(name="test_pipeline")
def test_pipeline(message: str) -> str:
    # Call the print_message component
    result = print_message(message=message)
    return result

# Compile the pipeline
compiler.Compiler().compile(test_pipeline, "test_pipeline.yaml")
```

This code snippet defines a Kubeflow Pipeline named `test_pipeline` with one component: `print_message`. The `print_message` component takes a string `message`, prints it, and returns the same string. The `test_pipeline` function calls `print_message` with an input string and returns its output. The pipeline is compiled into a YAML file named `test_pipeline.yaml`.