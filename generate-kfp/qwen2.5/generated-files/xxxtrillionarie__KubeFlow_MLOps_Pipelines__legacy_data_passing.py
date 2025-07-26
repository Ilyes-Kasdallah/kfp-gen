
from kfp import pipeline
from kfp.components import legacy_data_passing

@pipeline(name="data_passing_pipeline")
def data_passing_pipeline():
    # Define the producer component
    produce_anything = legacy_data_passing(
        input_file_path="/path/to/output/file",
        output_file_path="/path/to/output/file"
    )

    # Define the consumer component
    consume_anything = legacy_data_passing(
        input_file_path="/path/to/output/file",
        output_file_path="/path/to/output/file"
    )

    # Define the pipeline parameters
    parameter1 = "value1"
    parameter2 = "value2"

    # Define the pipeline steps
    produce_anything()
    consume_anything()

    # Define the pipeline execution
    return produce_anything(), consume_anything()

# Example usage
if __name__ == "__main__":
    result = data_passing_pipeline()
    print(result)
