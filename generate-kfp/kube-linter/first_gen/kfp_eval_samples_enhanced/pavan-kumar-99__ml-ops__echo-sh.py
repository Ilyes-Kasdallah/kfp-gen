from kfp import components
from kfp.dsl import pipeline


@pipeline(name="my-pipeline")
def my_pipeline():
    # Define the echo component
    echo_component = components.Component(
        name="echo",
        image="alpine",
        command=["echo", "Hi Kubeflow"],
    )

    # Use the echo component in the pipeline
    result = echo_component()

    return result
