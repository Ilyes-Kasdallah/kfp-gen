import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from src.steps.tokenize.pipeline_step import tokenize


@pipeline(name="Pipeline")
def tokenize_pipeline(reddit_train_csv):
    """
    This pipeline performs a machine learning task on a Reddit response dataset.

    Args:
    reddit_train_csv (str): The path to the Reddit training dataset CSV file.

    Returns:
    str: A message indicating the success of the pipeline execution.
    """
    # Tokenize the Reddit training dataset
    result = tokenize(reddit_train_csv)

    # Return the result
    return result


# Example usage
if __name__ == "__main__":
    # Define the input parameters
    input_data = "path/to/reddit_train.csv"

    # Call the pipeline function
    output = tokenize_pipeline(input_data)

    # Print the output
    print(output)
