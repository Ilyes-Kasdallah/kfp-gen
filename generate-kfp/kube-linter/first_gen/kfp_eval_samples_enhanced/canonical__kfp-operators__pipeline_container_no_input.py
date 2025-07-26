from kfp import components
from kfp.dsl import pipeline


@dsl.pipeline(name="v2-container-component-no-input")
def pipeline_container_no_input():
    # Define the container_no_input component
    container_no_input = components.container_no_input(
        image="python:3.7", command=["echo", "hello world"]
    )

    # Return the container_no_input component
    return container_no_input
