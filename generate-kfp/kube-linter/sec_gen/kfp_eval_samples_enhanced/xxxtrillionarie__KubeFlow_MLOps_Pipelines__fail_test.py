import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the V1 legacy engine
@dsl.component
def fail_v1():
    # Simulate a failure by raising an exception
    raise Exception("This is a test failure")


# Define the V2 engine
@dsl.component
def fail_v2():
    # Simulate a failure by raising an exception
    raise Exception("This is a test failure")


# Define the pipeline function
@dsl.pipeline(name="fail_pipeline")
def fail_test():
    # Use the V1 legacy engine
    result_v1 = fail_v1()

    # Use the V2 engine
    result_v2 = fail_v2()

    # Return the results of both components
    return result_v1, result_v2


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(fail_test, pipeline_root)
