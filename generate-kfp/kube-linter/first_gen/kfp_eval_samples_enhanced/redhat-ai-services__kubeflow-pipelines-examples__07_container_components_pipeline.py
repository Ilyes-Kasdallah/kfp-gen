from kfp import components
from kfp.dsl import pipeline


@pipeline(name="container-pipeline")
def container_pipeline(a=1.0, b=7.0):
    # Define the add component
    add = components.add()

    # Execute the add component with the provided inputs
    result = add(a, b)

    # Return the result
    return result
