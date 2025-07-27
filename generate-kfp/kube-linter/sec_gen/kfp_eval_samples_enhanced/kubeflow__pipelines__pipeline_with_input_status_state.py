import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline with input status state
@dsl.pipeline(
    name="status_state_pipeline", description="A simple pipeline with an exit handler"
)
def pipeline_with_input_status_state():
    # Define the echo_state component
    @component
    def echo_state(status):
        # Print the status of the previous pipeline task
        print(f"Previous task status: {status}")
        # Return a dummy output
        return Output("dummy_output")

    # Define the main task that will trigger the echo_state component
    @component
    def main_task():
        # Simulate a task that triggers the echo_state component
        # For demonstration purposes, we'll just print a message
        print("Main task is running...")
        # Trigger the echo_state component
        echo_state(status="success")

    # Define the pipeline
    @pipeline_with_input_status_state
    def pipeline():
        # Main task
        main_task()


# Compile the pipeline
pipeline.compile()
