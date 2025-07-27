import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the PVC component
@component(name="10_mount_pvc_pipeline")
def mount_pvc():
    # Mount the PVC at /opt/data
    return Dataset(name="my-data", path="/opt/data")


# Define the add component
@component(name="add")
def add(a: float, b: float):
    # Calculate the sum of a and b
    return a + b


# Define the pipeline
@pipeline(
    name="PVC Pipeline", description="Two additions with a Persistent Volume Claim"
)
def pvcc_pipeline():
    # Call the add component with hardcoded b=4.0
    result = add(4.0, 4.0)

    # Output the result
    return Output("result", result)


# Compile the pipeline
pvcc_pipeline.compile()
