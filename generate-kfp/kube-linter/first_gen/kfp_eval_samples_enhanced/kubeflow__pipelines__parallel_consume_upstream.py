from kfp import pipeline
from kfp.dsl import component


@component
def split_input(input_str: str) -> list:
    """
    Splits a comma-separated string into a list of strings.

    Args:
    input_str (str): A comma-separated string.

    Returns:
    list: A list of strings from the input string.
    """
    return input_str.split(",")


@pipeline(name="loop_consume_upstream")
def loop_consume_upstream():
    """
    Performs a series of file operations within a parallel loop.

    Steps:
    - split_input: Takes a comma-separated string as input and splits it into a list of strings.
    """
    # Example usage
    result = split_input("component1,component2,component3")
    print(result)


# Run the pipeline
loop_consume_upstream()
