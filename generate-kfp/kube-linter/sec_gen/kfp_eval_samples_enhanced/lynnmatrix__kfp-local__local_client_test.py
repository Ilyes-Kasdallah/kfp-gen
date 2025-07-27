import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the local client test pipeline
@pipeline(name="test-run-local-pipeline")
def local_client_test():
    # Define the hello component
    @component
    def hello(name):
        return f"hello {name}"

    # Define the main task: run the hello component
    @component
    def main_task():
        result = hello("world")
        return result

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Define the pipeline
    pipeline(
        name="test-run-local-pipeline",
        steps=[
            main_task(),
        ],
        output_dir=pipeline_root,
    )
