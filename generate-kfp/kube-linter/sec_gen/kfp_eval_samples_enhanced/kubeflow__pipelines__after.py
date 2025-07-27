import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the Print Text component
@component
def print_text(text: str) -> None:
    """Prints the given text to standard output."""
    print(text)


# Define the pipeline
@pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Define the first task
    @component
    def task1(text: str) -> None:
        """Prints the given text to standard output."""
        print_text(text)

    # Define the second task
    @component
    def task2(text: str) -> None:
        """Prints the given text to standard output."""
        print_text(text)

    # Define the third task
    @component
    def task3(text: str) -> None:
        """Prints the given text to standard output."""
        print_text(text)

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Define the pipeline
    pipeline(
        name="pipeline-with-after",
        steps=[
            task1("Hello"),
            task2("World"),
            task3("KFP"),
        ],
        pipeline_root=pipeline_root,
    )
