import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the first component
@component
def first_component():
    # Generate two strings: "first" and "second"
    return "first", "second"


# Define the second component
@component
def second_component():
    # Follow these rules to ensure correctness
    return "result1", "result2"


# Define the pipeline
@pipeline(name="lightweight_python_functions_v2_with_outputs")
def lightweight_python_functions_v2_with_outputs():
    # Call the first component
    result1, result2 = first_component()

    # Call the second component
    output1, output2 = second_component()

    # Return the results as outputs
    return {"result1": output1, "result2": output2}


# Run the pipeline
if __name__ == "__main__":
    pipeline_root = "gs://my-bucket/pipeline-root"
    pipeline(lightweight_python_functions_v2_with_outputs, pipeline_root=pipeline_root)
