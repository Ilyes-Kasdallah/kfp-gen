import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function with parameters
@dsl.pipeline(name="pipeline-with-pipelineparam-containing-format")
def pipeline_with_pipelineparam_containing_format():
    # Define the first component: print_op
    @component
    def print_op(name):
        # Print the input string to the standard output
        print(f"Printing: {name}")
        # Return the input string as its output
        return name

    # Define the second component: print_op
    @component
    def print_op(name):
        # Print the input string to the standard output
        print(f"Printing: {name}")
        # Return the input string as its output
        return name


# Example usage of the pipeline function
if __name__ == "__main__":
    # Create a pipeline root directory
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Compile the pipeline
    kfp.compiler.Compiler().compile(
        pipeline_with_pipelineparam_containing_format, pipeline_root
    )
