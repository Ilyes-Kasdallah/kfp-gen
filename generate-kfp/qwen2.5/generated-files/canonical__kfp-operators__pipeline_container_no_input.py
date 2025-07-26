
from kfp import pipeline, component

@pipeline(name="v2-container-component-no-input")
def pipeline_container_no_input():
    # Define the container_no_input component
    container_no_input = component.Component(
        name="container_no_input",
        image="python:3.7",
        command=["echo", "hello world"],
        inputs={},
        outputs={}
    )

    # Return the pipeline function
    return container_no_input
