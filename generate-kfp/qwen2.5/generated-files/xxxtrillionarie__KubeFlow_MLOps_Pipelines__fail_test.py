
from kfp import dsl

@dsl.pipeline(name="fail_pipeline")
def fail_pipeline():
    # Define the first version of the pipeline
    v1_pipeline = dsl.Pipeline(
        name="v1_pipeline",
        steps=[
            dsl.component(
                name="fail",
                image="gcr.io/kubeflow/pipelines:latest",
                command=["python", "fail.py"],
                inputs={
                    "input": "test_input"
                },
                outputs={"output": "test_output"}
            )
        ]
    )

    # Define the second version of the pipeline
    v2_pipeline = dsl.Pipeline(
        name="v2_pipeline",
        steps=[
            dsl.component(
                name="fail",
                image="gcr.io/kubeflow/pipelines:latest",
                command=["python", "fail.py"],
                inputs={
                    "input": "test_input"
                },
                outputs={"output": "test_output"}
            )
        ]
    )

    # Combine the two pipelines
    return v1_pipeline + v2_pipeline

# Function to test the pipeline's failure handling
@dsl.component
def fail_test():
    # Simulate a failure by raising an exception
    raise Exception("Test failed")

# Run the pipeline
result = fail_pipeline()
print(result)
