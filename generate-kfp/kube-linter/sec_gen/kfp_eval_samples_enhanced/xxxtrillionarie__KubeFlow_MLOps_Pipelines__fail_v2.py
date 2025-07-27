import sys
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@dsl.component
def fail():
    # Simulate a failure by exiting with a return code of 1
    sys.exit(1)


@dsl.pipeline(name="fail-pipeline")
def fail_pipeline():
    # Execute the 'fail' component once
    fail()
