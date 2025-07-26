import kfp
from kfp.dsl import pipeline, component


@component
def preprocess_data(data):
    """
    Preprocesses the input data.

    Args:
    data (str): The input data to be processed.

    Returns:
    str: The preprocessed data.
    """
    # Example preprocessing logic
    return data.upper()


@pipeline(name="A Simple CI Pipeline")
def simple_ci_pipeline():
    """
    A simple CI pipeline that uses the preprocess_data component.
    """
    # Step 1: Input data
    input_data = "Hello, World!"

    # Step 2: Preprocess the data
    processed_data = preprocess_data(input_data)

    # Step 3: Output the processed data
    print(processed_data)


# Run the pipeline
simple_ci_pipeline()
