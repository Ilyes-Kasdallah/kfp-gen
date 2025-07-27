import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the split_ids component
@component
def split_ids(model_ids: str) -> List[str]:
    """
    Splits a comma-separated string of model IDs into individual IDs.

    Args:
    model_ids (str): A comma-separated string of model IDs.

    Returns:
    List[str]: A list of individual IDs.
    """
    return model_ids.split(",")


# Define the collecting_artifacts pipeline
@pipeline(name="collecting_artifacts")
def collecting_artifacts(
    model_ids: str = "model1,model2,model3",
    output_dataset: Dataset[str] = "output_dataset",
    output_model: Model[str] = "output_model",
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    """
    Collects model artifacts from a comma-separated string of model IDs.

    Args:
    model_ids (str): A comma-separated string of model IDs.
    output_dataset (Dataset[str]): The dataset to store the collected artifacts.
    output_model (Model[str]): The model to store the collected artifacts.
    cache (bool): Whether to cache the results.
    retries (int): The number of retries for failed tasks.
    resource_limits (dict): The resource limits for the pipeline.

    Returns:
    None
    """
    # Split the input model IDs
    ids = split_ids(model_ids)

    # Create a dataset from the split IDs
    dataset = Dataset.from_items(ids)

    # Create a model from the split IDs
    model = Model.from_items(ids)

    # Cache the results
    if cache:
        dataset.cache()

    # Set retries
    dataset.retry(retries)

    # Set resource limits
    dataset.resource_limits(resource_limits)

    # Output the dataset and model
    Output(dataset=dataset, model=output_model)


# Compile the pipeline
kfp.compiler.Compiler().compile(collecting_artifacts)
