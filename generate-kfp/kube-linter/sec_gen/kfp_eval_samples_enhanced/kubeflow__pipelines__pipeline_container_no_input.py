import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="v2-container-component-no-input")
def pipeline_container_no_input():
    # Define the container_no_input component
    container_no_input = component(
        name="container_no_input",
        image="python:3.7",
        command=["echo", "hello world"],
        inputs={},
        outputs={},
        cache=True,
        retries=2,
        resource_limits={"cpu": "1", "memory": "1Gi"},
    )

    # Return the container_no_input component
    return container_no_input


# Example usage of the pipeline function
if __name__ == "__main__":
    # Execute the pipeline
    pipeline_container_no_input()
