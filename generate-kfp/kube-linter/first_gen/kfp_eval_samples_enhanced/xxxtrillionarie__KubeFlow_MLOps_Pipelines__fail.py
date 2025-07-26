from kfp import components
from kfp.dsl import pipeline


@pipeline(name="fail-pipeline")
def fail_pipeline():
    # Define the fail_task component
    @components.component(
        name="fail_task",
        description="This component intentionally exits with a return code of 1.",
        image="alpine:latest",
    )
    def fail_task():
        # Simulate a failure by raising an exception
        raise Exception("Simulated failure")


# Run the pipeline
if __name__ == "__main__":
    fail_pipeline()
