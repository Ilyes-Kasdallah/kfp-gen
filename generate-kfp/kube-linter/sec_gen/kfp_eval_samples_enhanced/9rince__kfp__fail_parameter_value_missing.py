import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@component
def Echo(text: str) -> None:
    """Echoes the input text to standard output."""
    print(text)


@pipeline(name="parameter_value_missing")
def parameter_value_missing(parameter: str):
    """Runs the Echo component with the provided parameter."""
    Echo(parameter)
