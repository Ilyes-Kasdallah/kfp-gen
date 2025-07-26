import kfp
from kfp.dsl import component, pipeline


@dsl.pipeline(name="_artifact_location")
def simple_pipeline():
    # Define the echo_workflow_vars component
    @component
    def echo_workflow_vars():
        print(f"Workflow Name: {kfp.context.workflow.name}")

    # Define the main task that uses the echo_workflow_vars component
    @component
    def main_task():
        echo_workflow_vars()


# Run the pipeline
simple_pipeline()
