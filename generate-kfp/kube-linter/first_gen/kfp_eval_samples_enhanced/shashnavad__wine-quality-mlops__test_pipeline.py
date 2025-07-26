import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from great_expectations import expectations_registry
from great_expectations.exceptions import ExpectationError


# Define the pipeline
@pipeline(name="wine_quality_pipeline")
def wine_quality_pipeline():
    # Define the validate_data component
    @component
    def validate_data(input_file_path):
        # Load the data from the CSV file
        data = kfp.io.textfile.read_csv(input_file_path)

        # Validate the data using Great Expectations
        try:
            expectations_registry.validate(data)
            print("Data validation passed.")
        except ExpectationError as e:
            print(f"Data validation failed: {e}")
            raise e

    # Define the main component that orchestrates the pipeline
    @component
    def main():
        # Call the validate_data component
        validate_data("path/to/wine_quality_dataset.csv")

    # Define the test_pipeline function
    @test_pipeline
    def test_pipeline():
        # Execute the main component
        main()


# Run the test_pipeline function
test_pipeline()
