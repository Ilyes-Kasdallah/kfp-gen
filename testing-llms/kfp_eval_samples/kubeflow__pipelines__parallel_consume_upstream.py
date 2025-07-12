```python
import kfp
from kfp import dsl

# Define the split_input component
@dsl.component(
    base_image='ubuntu',
    enable_caching=False,
    output_artifact_type=dsl.Artifact(type_name='list', schema=dsl.ArraySchema(str))
)
def split_input(input: str) -> list:
    return input.split(',')

# Define the create_file component
@dsl.component(
    base_image='ubuntu',
    enable_caching=False,
    output_artifact_type=dsl.Artifact(type_name='string')
)
def create_file(content: str, file: dsl.Output[Artifact]) -> None:
    with open(file.path, 'w') as f:
        f.write(content)

# Define the read_file component
@dsl.component(
    base_image='ubuntu',
    enable_caching=False,
    output_artifact_type=dsl.Artifact(type_name='string')
)
def read_file(file: dsl.Input[Artifact]) -> str:
    with open(file.path, 'r') as f:
        return f.read()

# Define the print_input component
@dsl.component(
    base_image='ubuntu',
    enable_caching=False,
    output_artifact_type=dsl.Artifact(type_name='list', schema=dsl.ArraySchema(str))
)
def print_input(input: list) -> None:
    for item in input:
        print(item)

# Define the parallel_consume_upstream pipeline
@dsl.pipeline(name='parallel_consume_upstream')
def parallel_consume_upstream():
    # Split the input string into a list of strings
    split_output = split_input(input='component1,component2,component3')

    # Iterate over the list of models in parallel
    with dsl.ParallelFor(split_output.output) as model_id:
        # Create a file with the model ID as content
        create_file(content=model_id, file=f'model_{model_id}.txt')

        # Read the file created in the previous step
        read_output = read_file(file=f'model_{model_id}.txt')

        # Print the model ID
        print_input(input=[model_id])

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(parallel_consume_upstream, package_path='parallel_consume_upstream.yaml')
```

This code snippet defines the required components and the pipeline structure, ensuring it meets the requirements specified in the question.