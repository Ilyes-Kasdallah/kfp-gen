import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="add_pipeline")
def add_pipeline(a: float = 0.0, b: float = 4.0):
    # Define the add component
    @component
    def add(a: float, b: float) -> float:
        return a + b

    # Call the add component with the provided parameters
    result = add(a, b)
    return result


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiled_pipeline = kfp.compiler.Compiler().compile(add_pipeline, pipeline_root)
