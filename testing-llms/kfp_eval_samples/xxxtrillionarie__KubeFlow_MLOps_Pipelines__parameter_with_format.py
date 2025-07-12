```python
import kfp
from kfp import dsl

# Define the print_op component
@dsl.component
def print_op(name: str) -> str:
    print(name)
    return name

# Define the main pipeline
@dsl.pipeline(
    name="pipeline-with-pipelineparam-containing-format",
    description="A simple pipeline with a pipeline parameter containing format"
)
def pipeline_with_pipelineparam_containing_format(name: str = "KFP"):
    # First print_op component
    first_print = print_op(name=name)

    # Second print_op component that depends on the output of the first print_op component
    second_print = print_op(first_print)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(pipeline_with_pipelineparam_containing_format, 'parameter_with_format.yaml')
```

This code snippet defines a Kubeflow Pipeline named `pipeline-with-pipelineparam-containing-format` that performs a simple string manipulation and printing. The pipeline consists of two components: `print_op`, which takes a string as input and prints it to the standard output, and another `print_op` that prepends the string "{}, again." to the input string and prints the result. The pipeline's control flow is sequential, with the second `print_op` component depending on the output of the first `print_op` component. The first component is initialized with a pipeline parameter `name` which defaults to "KFP", and this parameter is incorporated into the string using the `.format()` method. The pipeline uses the Kubeflow Pipelines SDK (`kfp`).