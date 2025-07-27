import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the echo component
@component
def echo(input_str: str) -> str:
    return input_str


# Define the pipeline
@pipeline(name="echo-pipeline")
def test_cli():
    # Execute the echo component once
    result = echo("Hello, world!")
    print(result)


# Run the pipeline
test_cli()
