import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@component
def fail_parameter_value_missing(text):
    """Echoes the input text."""
    print(text)
    return text


@pipeline(name="parameter_value_missing")
def parameter_value_missing():
    """Runs the fail_parameter_value_missing component."""
    result = fail_parameter_value_missing("Hello, World!")
    return result


# Example usage
if __name__ == "__main__":
    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Compile the pipeline
    compiler = kfp.compiler.Compiler()
    compiled_pipeline = compiler.compile(
        parameter_value_missing, pipeline_root=pipeline_root
    )

    # Print the compiled pipeline
    print(compiled_pipeline)
