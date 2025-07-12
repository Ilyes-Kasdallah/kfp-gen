```python
import kfp
from kfp import dsl

# Import necessary libraries
import pandas as pd
import json

# Define the concat_message component
@dsl.component(
    base_image='python:3.8-slim',
    packages_to_install=['pandas'],
    outputs=[
        dsl.Output('result', type=dsl.String)
    ]
)
def concat_message(first: str, second: str) -> str:
    result = first + " " + second
    return result

# Define the add_numbers component
@dsl.component(
    base_image='python:3.8-slim',
    packages_to_install=['numpy'],
    outputs=[
        dsl.Output('result', type=dsl.Integer)
    ]
)
def add_numbers(first: int, second: int) -> int:
    result = first + second
    return result

# Define the output_artifact component
@dsl.component(
    base_image='python:3.8-slim',
    packages_to_install=['pandas'],
    outputs=[
        dsl.Output('dataset', type=dsl.Dataset)
    ]
)
def output_artifact(number: int, message: str) -> dsl.Dataset:
    data = [message] * number
    df = pd.DataFrame(data)
    dataset = dsl.Artifact(type=dsl.Dataset, uri=df.to_csv(index=False))
    return dataset

# Define the output_named_tuple component
@dsl.component(
    base_image='python:3.8-slim',
    packages_to_install=['pandas'],
    outputs=[
        dsl.Output('named_tuple', type=dsl.NamedTuple)
    ]
)
def output_named_tuple(dataset: dsl.Dataset) -> dsl.NamedTuple:
    df = pd.read_csv(dataset.uri)
    scalar = df.iloc[0][0]
    metrics = json.dumps({'key': 'value'})
    model = '{"content": "model content"}'
    named_tuple = dsl.NamedTuple(scalar=scalar, metrics=metrics, model=model)
    return named_tuple

# Define the lightweight_python_functions_v2_with_outputs pipeline
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

    # Output of concat_message and add_numbers as inputs to output_artifact
    dataset = output_artifact(add_result, concat_result)

    # Output of output_artifact as input to output_named_tuple
    named_tuple = output_named_tuple(dataset)

# Compile the pipeline
compiler.Compiler().compile(lightweight_python_functions_v2_with_outputs, 'lightweight_python_functions_v2_with_outputs.yaml')
```

This code snippet defines a Kubeflow Pipeline named `functions-with-outputs` that performs the specified operations and outputs the results as required.