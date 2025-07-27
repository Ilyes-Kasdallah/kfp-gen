import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the legacy_exit_handler function
@component
def legacy_exit_handler(url: Input[str]) -> Output[Dataset]:
    # Placeholder for actual data download logic
    # For demonstration, we'll just return a dummy dataset
    return Dataset.from_tensor_slices({"data": [1, 2, 3, 4, 5]})


# Define the Exit Handler pipeline
@pipeline(name="Exit Handler")
def exit_handler_pipeline():
    # Task 1: Download data from GCS
    data = legacy_exit_handler("gs://my-bucket/data.csv")

    # Task 2: Print the downloaded data
    print(data)


# Compile the pipeline
exit_handler_pipeline.compile()
