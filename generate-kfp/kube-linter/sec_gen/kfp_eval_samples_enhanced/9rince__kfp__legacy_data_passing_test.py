import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the legacy_data_passing_test function
@component
def legacy_data_passing_test(
    input_dataset: Dataset,
    output_model: Model,
    cache_key: str = None,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Simulate data passing operation
    # For demonstration, we'll just print the input and output
    print(f"Input dataset: {input_dataset}")
    print(f"Output model: {output_model}")
    print(f"Cache key: {cache_key}")
    print(f"Retries: {retries}")
    print(f"Resource limits: {resource_limits}")


# Define the data_passing_pipeline function
@pipeline(name="data_passing_pipeline")
def data_passing_pipeline(
    input_dataset: Dataset,
    output_model: Model,
    cache_key: str = None,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Call the legacy_data_passing_test function
    legacy_data_passing_test(
        input_dataset, output_model, cache_key, retries, resource_limits
    )


# Example usage
if __name__ == "__main__":
    # Create a pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Execute the pipeline
    pipeline(data_passing_pipeline, pipeline_root)
