import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the component function
@component
def test_op(workflow_name):
    # Print the value of the environment variable WORKFLOW_NAME
    print(f"Workflow Name: {workflow_name}")


# Define the pipeline function
@pipeline(name="_artifact_location_test")
def test_pipeline():
    # Call the test_op function with the input 'WORKFLOW_NAME'
    test_op(workflow_name="test_pipeline")


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(test_pipeline)
