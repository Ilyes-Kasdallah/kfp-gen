
from kfp import dsl

@dsl.pipeline(name="fail-pipeline")
def fail_pipeline():
    # Define the task to be executed
    @dsl.component(name="fail_task")
    def fail_task():
        # Call the fail function from the Python script
        return fail()

# Execute the pipeline
fail_pipeline()
