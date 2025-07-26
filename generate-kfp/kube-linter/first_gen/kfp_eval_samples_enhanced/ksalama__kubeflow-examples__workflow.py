from kfp import workflow
from kfp.dsl import component


@component
def add_op(x_value: int, y_value: int) -> int:
    """
    Adds two integers and returns their sum.

    Args:
    x_value (int): The first integer.
    y_value (int): The second integer.

    Returns:
    int: The sum of x_value and y_value.
    """
    return x_value + y_value


@component
def multiply_op(x_value: int, y_value: int) -> int:
    """
    Multiplies two integers and returns their product.

    Args:
    x_value (int): The first integer.
    y_value (int): The second integer.

    Returns:
    int: The product of x_value and y_value.
    """
    return x_value * y_value


@component
def divide_op(x_value: int, y_value: int) -> float:
    """
    Divides two integers and returns their quotient.

    Args:
    x_value (int): The first integer.
    y_value (int): The second integer.

    Returns:
    float: The quotient of x_value and y_value.
    """
    if y_value == 0:
        raise ValueError("Cannot divide by zero.")
    return x_value / y_value


@dsl.pipeline(name="A Simple CI Pipeline")
def simple_ci_pipeline():
    # Step 1: Add two integers
    result_add = add_op(5, 3)
    print(f"Result of add_op(5, 3): {result_add}")

    # Step 2: Multiply two integers
    result_multiply = multiply_op(4, 6)
    print(f"Result of multiply_op(4, 6): {result_multiply}")

    # Step 3: Divide two integers
    result_divide = divide_op(10, 2)
    print(f"Result of divide_op(10, 2): {result_divide}")


# Run the pipeline
simple_ci_pipeline()
