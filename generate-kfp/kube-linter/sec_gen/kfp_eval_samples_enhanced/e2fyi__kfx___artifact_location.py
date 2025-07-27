import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="_artifact_location")
def simple_pipeline():
    # Define the echo_workflow_vars component
    @component
    def echo_workflow_vars(workflow_name):
        # Print the value of the WORKFLOW_NAME environment variable
        print(f"Workflow Name: {workflow_name}")

    # Define the main task that depends on the echo_workflow_vars component
    @component
    def main_task():
        # Use the set_workflow_env function to inject the workflow name as an environment variable
        set_workflow_env(workflow_name)

        # Example task that can be executed after the main task
        print("Executing example task...")

    # Define the main task as a pipeline step
    main_task()


# Compile the pipeline
kfp.compiler.Compiler().compile(simple_pipeline)
