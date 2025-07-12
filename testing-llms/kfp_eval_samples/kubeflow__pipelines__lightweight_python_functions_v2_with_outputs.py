```python
from kfp import dsl
from typing import NamedTuple

# Define a custom named tuple for the output
Metrics = NamedTuple('Metrics', [('accuracy', float)])

# Define the components
@dsl.component
def concat_message(first: str, second: str) -> str:
    return first + second

@dsl.component
def add_numbers(first: int, second: int) -> int:
    return first + second

@dsl.component
def output_artifact(number: int, message: str) -> dsl.DatasetArtifact:
    dataset = dsl.DatasetArtifact()
    for _ in range(number):
        dataset.add_row(message)
    return dataset

@dsl.component
def output_named_tuple(artifact: dsl.DatasetArtifact) -> NamedTuple:
    # Assuming the Dataset contains a single row with a string field named 'content'
    content = artifact.get_rows()[0]['content']
    return Metrics(accuracy=0.85), Metrics(accuracy=0.90), f"Model contents:{content}"

# Define the pipeline
@dsl.pipeline(name="functions-with-outputs")
def lightweight_python_functions_v2_with_outputs(
    first_message: str = 'first',
    second_message: str = 'second',
    first_number: int = 1,
    second_number: int = 2
):
    # Parallel execution of concat_message and add_numbers
    concat_result = concat_message(first_message, second_message)
    add_result = add_numbers(first_number, second_number)

    # Dependency on output_artifact
    output_dataset = output_artifact(add_result, concat_result)

    # Dependency on output_named_tuple
    output_metrics, output_model = output_named_tuple(output_dataset)

    # Output the results
    print(f"Concatenated Message: {concat_result}")
    print(f"Sum of Numbers: {add_result}")
    print(f"Metrics: {output_metrics}")
    print(f"Model: {output_model}")

# Execute the pipeline
if __name__ == "__main__":
    from kfp.compiler import.Compiler
    compiler = Compiler()
    pipeline_spec = compiler.compile(lightweight_python_functions_v2_with_outputs, package_path='lightweight_python_functions_v2_with_outputs.yaml')
```

This code snippet defines a Kubeflow Pipeline named `functions-with-outputs` that performs the specified operations and outputs the results. The pipeline includes four components: `concat_message`, `add_numbers`, `output_artifact`, and `output_named_tuple`. The pipeline's control flow ensures that the operations are executed in parallel and that the final outputs are correctly handled.