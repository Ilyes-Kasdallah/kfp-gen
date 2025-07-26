from kfp import pipeline
from kfp.dsl import component

# Define the base image
image = "image-registry.openshift-image-registry"


@component
def return_multiple_values(a: float, b: float) -> tuple:
    """
    Returns a tuple containing the sum and product of two float inputs.

    Args:
    a (float): The first input.
    b (float): The second input.

    Returns:
    tuple: A tuple containing the sum and product of the inputs.
    """
    return (a + b, a * b)


# Define the pipeline
with pipeline("Submitted Pipeline") as p:
    # Add the first component
    p.add_component(return_multiple_values, name="return_multiple_values")

    # Add the second component
    p.add_component(return_multiple_values, name="return_multiple_values")

# Run the pipeline
p.run()
