import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the collected_parameters component
@component
def collected_parameters(model_ids: str) -> List[str]:
    """
    Splits a comma-separated string of model IDs into a list of individual IDs.

    Args:
    model_ids (str): A comma-separated string of model IDs.

    Returns:
    List[str]: A list of individual model IDs.
    """
    # Split the input string by commas and return the resulting list
    return model_ids.split(",")


# Define the pipeline
@pipeline(name="collected_param_pipeline")
def collected_param_pipeline():
    """
    Performs a series of operations on a list of model IDs.

    Steps:
    1. Call the `split_ids` component with the input "s1,s2,s3".
    2. Print the output of the `split_ids` component.
    """
    # Call the split_ids component with the input "s1,s2,s3"
    model_ids = collected_parameters("s1,s2,s3")

    # Print the output of the split_ids component
    print(model_ids)


# Compile the pipeline
compiled_pipeline = kfp.compiler.Compiler().compile(collected_param_pipeline)
