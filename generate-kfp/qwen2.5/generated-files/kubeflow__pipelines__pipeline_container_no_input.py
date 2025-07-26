
from kfp import dsl

@dsl.pipeline(name="v2-container-component-no-input")
def pipeline_container_no_input():
    # Define the container component
    container_no_input = dsl.container(
        image="python:3.7",
        command=["echo", "hello world"],
        inputs={}
    )

    # Return the pipeline
    return container_no_input
