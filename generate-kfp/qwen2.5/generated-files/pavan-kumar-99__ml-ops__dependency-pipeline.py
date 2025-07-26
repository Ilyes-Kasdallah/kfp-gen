
from kfp import dsl

@dsl.pipeline(name="my-pipeline")
def my_pipeline():
    # Step 1: Execute the echo component
    echo_component = dsl.component(
        name="echo",
        image="alpine",
        command=["echo", "Hi Kubeflow"],
        dependencies=[],
    )

    # Step 2: Execute the echo component again
    echo_component = dsl.component(
        name="echo",
        image="alpine",
        command=["echo", "Hi Kubeflow"],
        dependencies=[echo_component],
    )

# Example usage of the pipeline
if __name__ == "__main__":
    my_pipeline()
