import kfp
from kfp.dsl import pipeline, component


@component
def test_op():
    """Prints the value of the environment variable WORKFLOW_NAME."""
    print(f"WORKFLOW_NAME: {kfp.context.workflow.name}")


@pipeline(name="_artifact_location_test")
def test_pipeline():
    """Runs the test_op component."""
    test_op()


# Run the pipeline
test_pipeline()
