import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@component
def hello_world(text="hi there"):
    """Function to greet the user."""
    print(text)
    return text


@pipeline(name="hello-world")
def hello_world_pipeline():
    """Pipeline to demonstrate greeting."""
    # Task 1: Pass the input text to hello_world
    result = hello_world(text=text)

    # Task 2: Return the result of hello_world
    return result


# Example usage
if __name__ == "__main__":
    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Compile the pipeline
    kfp.compiler.Compiler().compile(hello_world_pipeline, pipeline_root)
