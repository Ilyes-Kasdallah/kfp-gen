from kfp import components
from kfp.dsl import pipeline


@pipeline(name="fail_pipeline")
def fail_pipeline():
    # Define the fail_task function
    @components.function(name="fail_task")
    def fail_task():
        # Simulate a pipeline failure by calling the fail function
        fail("Pipeline failed!")


# Run the pipeline
fail_pipeline()
