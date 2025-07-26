import kfp
from kfp.dsl import pipeline, component


@component
def parameter_with_format_test(name: str) -> str:
    """
    This function takes a string input and returns its length.

    Args:
    name (str): The input string to process.

    Returns:
    int: The length of the input string.
    """
    return len(name)


@pipeline(name="my_pipeline")
def my_pipeline():
    """
    This pipeline contains a single component that takes a string input and returns its length.
    """
    result = parameter_with_format_test("Hello, World!")
    print(f"The length of the input string is: {result}")


if __name__ == "__main__":
    my_pipeline()
