import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@dsl.component
def print_op(name: str) -> None:
    """Prints the given string to the standard output."""
    print(name)


@dsl.pipeline(name="pipeline-with-pipelineparam-containing-format")
def pipeline_with_pipelineparam_containing_format():
    """A simple pipeline that demonstrates string manipulation and printing."""
    # Define the first component
    print_op("Hello, World!")

    # Define the second component
    print_op("This is a test.")


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(
    pipeline_with_pipelineparam_containing_format, pipeline_root
)
