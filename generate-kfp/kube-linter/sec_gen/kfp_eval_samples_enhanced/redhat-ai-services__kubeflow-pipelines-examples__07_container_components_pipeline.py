import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="container-pipeline")
def container_pipeline(a=1.0, b=7.0):
    # Define the add component
    @component
    def add(a, b):
        return a + b

    # Define the main task
    @dsl.task(name="main-task")
    def main_task():
        # Execute the add component with the provided inputs
        result = add(a, b)
        return result


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(container_pipeline)

# Print the compiled pipeline
print(compiled_pipeline)
