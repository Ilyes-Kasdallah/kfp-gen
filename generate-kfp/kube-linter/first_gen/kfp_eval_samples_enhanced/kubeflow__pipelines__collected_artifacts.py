from kfp import pipeline
from kfp.dsl import component


@dsl.pipeline(name="collecting_artifacts")
def collecting_artifacts(model_ids):
    """
    Collects model IDs from a comma-separated string and processes them.

    Args:
    model_ids (str): A comma-separated string of model IDs.

    Returns:
    list: A list of individual model IDs.
    """
    # Split the input string into individual IDs
    individual_ids = model_ids.split(",")

    # Return the list of individual IDs
    return individual_ids


# Example usage
model_ids = "1,2,3,4,5,6,7,8,9"
result = collecting_artifacts(model_ids)
print(result)  # Output: ['1', '2', '3', '4', '5', '6', '7', '8', '9']
