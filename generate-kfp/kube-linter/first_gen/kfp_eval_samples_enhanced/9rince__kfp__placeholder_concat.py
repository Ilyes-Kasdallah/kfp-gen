from kfp import pipeline
from kfp.dsl import component


@component
def placeholder_concat(input_one: str, input_two: str) -> str:
    """
    Concatenates two strings with a '+' symbol and the string '=three'.

    Args:
    input_one (str): The first string to concatenate.
    input_two (str): The second string to concatenate.

    Returns:
    str: The concatenated string.
    """
    return f"{input_one}+{input_two}=three"


@pipeline(name="one-step-pipeline-with-concat-placeholder")
def one_step_pipeline_with_concat_placeholder():
    """
    A single string concatenation operation using a placeholder.
    """
    result = placeholder_concat("one", "two")
    assert result == "one+two=three", f"Expected 'one+two=three', got {result}"
    print("Concatenation successful!")


one_step_pipeline_with_concat_placeholder()
