
from kfp import dsl

@dsl.pipeline(name="Exit Handler")
def exit_handler(url="gs://ml-pipeline/shakespeare/shakespeare1.txt"):
    # Define the GCS download component
    download_component = dsl.component(
        name="GCS - Download",
        description="Downloads a text file from a Google Cloud Storage URL.",
        inputs={
            "url": dsl.input(default_value="gs://ml-pipeline/shakespeare/shakespeare1.txt")
        },
        outputs={
            "file_path": dsl.output()
        },
        steps=[
            dsl.task(
                name="Download File",
                description="Downloads the file from GCS.",
                command=["gsutil", "get", url, "-o", "file_path"]
            )
        ]
    )

    # Define the exit handler component
    exit_handler_component = dsl.component(
        name="Exit Handler",
        description="Handles the exit condition of the pipeline.",
        inputs={
            "exit_code": dsl.input(default_value=0)
        },
        outputs={
            "status": dsl.output()
        },
        steps=[
            dsl.task(
                name="Handle Exit Code",
                description="Handles the exit code of the pipeline.",
                command=["echo", f"Exit code: {exit_code}"]
            )
        ]
    )

    # Define the main pipeline
    @dsl.pipeline_function(name="Main Pipeline")
    def main_pipeline():
        # Execute the download component
        download_component.execute()

        # Execute the exit handler component with an exit code of 1
        exit_handler_component.execute(exit_code=1)

# Run the main pipeline
main_pipeline()
