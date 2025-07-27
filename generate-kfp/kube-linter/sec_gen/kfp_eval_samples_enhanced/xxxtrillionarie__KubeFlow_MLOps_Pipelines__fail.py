import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@component
def fail_task():
    # Simulate a failure by raising an exception
    raise Exception("Failed task")


@pipeline(name="fail-pipeline")
def fail_pipeline():
    # Call the fail_task component
    fail_task()


# Compile the pipeline
kfp.compiler.Compiler().compile(fail_pipeline)
