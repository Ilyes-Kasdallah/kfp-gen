```python
import kfp
from kfp import dsl

# Define the print_op component
@dsl.component(
    base_image='ubuntu:latest',
    outputs=['output'],
    parameters=[
        dsl.InputParameter(name='name', default='KFP')
    ]
)
def print_op(name):
    # Construct the formatted string
    formatted_string = f"Hello, {name}!"
    # Print the formatted string
    print(formatted_string)
    # Return the formatted string
    return formatted_string

# Define the main pipeline
@dsl.pipeline(
    name='pipeline-with-pipelineparam-containing-format'
)
def pipeline_with_pipelineparam_containing_format(name):
    # First print_op component
    first_print = print_op(name=name)
    
    # Second print_op component that uses the output of the first print_op component
    second_print = print_op(name=first_print.output)

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(pipeline_with_pipelineparam_containing_format)

# Submit the pipeline run
client = kfp.Client()
run = client.create_run_from_pipeline_func(compiled_pipeline, arguments={'name': 'World'})
```

This code snippet defines a Kubeflow Pipeline named `pipeline-with-pipelineparam-containing-format` that includes two components: `print_op` and `print_op` (a second instance). The pipeline takes a single string parameter `name` with a default value of 'KFP'. The first `print_op` component constructs a formatted string and prints it. The second `print_op` component uses the output of the first component and appends a string before printing. The pipeline is compiled and submitted to the Kubeflow Pipelines server.