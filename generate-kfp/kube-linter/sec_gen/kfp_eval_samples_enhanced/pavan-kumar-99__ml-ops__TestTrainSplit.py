import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="DataSplitPipeline")
def DataSplitPipeline(
    # Define the input dataset
    raw_data_path: Input[Dataset],
    # Define the output directory for the split dataset
    output_dir: Output[Dataset],
    # Define the number of splits
    num_splits: int,
    # Define the cache configuration
    cache_config: Output[Metrics],
    # Define the retry configuration
    retry_config: Output[Metrics],
    # Define the resource limits
    resource_limits: Output[Metrics],
):
    # Load the dataset from the remote YAML file
    raw_data = kfp.components.get_raw_data(raw_data_path)

    # Split the dataset into training and testing sets
    train_dataset, test_dataset = raw_data.split(num_splits=num_splits)

    # Save the training and testing datasets to the specified output directory
    train_dataset.save(output_dir)
    test_dataset.save(output_dir)

    # Enable caching
    cache_config.enable_cache()

    # Set retries
    retry_config.set_retries(max_retries=2)

    # Set resource limits
    resource_limits.cpu = "1"
    resource_limits.memory = "1Gi"
