import kfp
from kfp.dsl import Pipeline, PipelineTaskFinalStatus


@dsl.pipeline(name="status_state_pipeline")
def pipeline_with_input_status_state():
    # Define the echo_state component
    @dsl.component
    def echo_state(task_final_status: PipelineTaskFinalStatus):
        # Simulate an echo operation
        print(f"Echoing status: {task_final_status.status}")
        return task_final_status

    # Define the main pipeline task
    @dsl.component
    def main_task():
        # Simulate a task that depends on the echo state
        echo_status = echo_state(PipelineTaskFinalStatus("success"))
        print(f"Main task completed with status: {echo_status.status}")

    # Execute the main task
    main_task()
