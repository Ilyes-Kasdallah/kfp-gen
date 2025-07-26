
from kfp import pipeline
from kfp.components import pipeline_task

@dsl.pipeline(name="status_state_pipeline")
def status_state_pipeline():
    # Define the first component: echo_state
    @pipeline_task(name="echo_state")
    def echo_state(final_status):
        print(f"Echoing state: {final_status}")

    # Define the second component: exit_handler
    @pipeline_task(name="exit_handler")
    def exit_handler(final_status):
        print(f"Exiting with status: {final_status}")

    # Connect the two components with an exit handler
    exit_handler.connect(echo_state)

# Run the pipeline
status_state_pipeline()
