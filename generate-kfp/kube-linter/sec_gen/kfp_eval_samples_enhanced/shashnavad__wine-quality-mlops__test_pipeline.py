import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the validate_data component
@component
def validate_data(input_csv_path: Input[str]) -> Output[Metrics]:
    """
    Validates the input wine quality dataset using Great Expectations.

    Args:
    input_csv_path (str): Path to the CSV file containing the wine quality data.

    Returns:
    Output[Metrics]: A Metrics artifact containing validation metrics.
    """
    # Import necessary libraries
    import great_expectations as gex

    # Load the dataset
    df = gex.read_csv(input_csv_path)

    # Validate the dataset
    result = gex.validate(df)

    # Return the validation metrics
    return result


# Define the main pipeline
@pipeline(name="wine_quality_pipeline")
def test_pipeline():
    """
    Main pipeline function to execute the validate_data component.

    Returns:
    None
    """
    # Call the validate_data component
    validate_data_output = validate_data("path/to/wine_quality_dataset.csv")

    # Print the validation metrics
    print(validate_data_output)


# Compile the pipeline
test_pipeline()
