
from kfp import dsl

@dsl.pipeline(name="fail_pipeline")
def fail_pipeline():
    # Define the task that will fail
    @dsl.component(name="fail_task")
    def fail():
        print("Simulating a pipeline failure")
        return 1

# Execute the pipeline
fail_pipeline()
