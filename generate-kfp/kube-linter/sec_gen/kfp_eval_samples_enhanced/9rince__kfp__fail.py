import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@component
def fail_task():
    """Simulates a pipeline failure by returning a return code of 1."""
    return 1


@pipeline(name="fail_pipeline", description="A simple failure test using kfp")
def fail_pipeline():
    """Runs the fail_task component."""
    # Simulate a pipeline failure by calling fail_task
    result = fail_task()
    print(f"Result of fail_task: {result}")


# Example usage
if __name__ == "__main__":
    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Compile the pipeline
    kfp.compiler.Compiler().compile(fail_pipeline, pipeline_root)
