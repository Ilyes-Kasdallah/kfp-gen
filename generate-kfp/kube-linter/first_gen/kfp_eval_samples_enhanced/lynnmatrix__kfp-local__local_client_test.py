from kfp import pipeline
from kfp.dsl import component


@component
def hello(name: str) -> str:
    """Returns 'hello ' concatenated with the input name."""
    return f"hello {name}"


@pipeline(name="test-run-local-pipeline")
def test_run_local_pipeline():
    """Runs the hello component on a local machine."""
    result = hello("world")
    print(result)


# Run the pipeline locally
test_run_local_pipeline()
