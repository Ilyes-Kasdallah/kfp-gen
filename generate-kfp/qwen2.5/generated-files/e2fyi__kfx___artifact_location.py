
from kfp import dsl

@dsl.pipeline(name="_artifact_location")
def simple_pipeline():
    # Define the echo_workflow_vars component
    @dsl.component
    def echo_workflow_vars():
        # Print the value of the WORKFLOW_NAME environment variable
        print(f"Workflow Name: {dsl.artifact_location}")
    
    # Execute the echo_workflow_vars component
    echo_workflow_vars()
