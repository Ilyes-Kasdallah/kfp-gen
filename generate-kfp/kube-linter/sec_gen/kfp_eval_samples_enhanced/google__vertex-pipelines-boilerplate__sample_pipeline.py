import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="sample-pipeline")
def sample_pipeline(message: str, gcs_filepath: str):
    # Create a component task for saving the message to GCS
    save_message_to_file = component(
        name="_save_message_to_file",
        description="Saves a message to GCS",
        inputs={"message": Input(str), "gcs_filepath": Input(str)},
        outputs={"output": Output(Dataset(type=DatasetType.FILE))},
        steps=[
            {
                "task": "write_to_gcs",
                "inputs": {
                    "message": {"value": message},
                    "gcs_filepath": {"value": gcs_filepath},
                },
                "outputs": {"output": {"type": DatasetType.FILE}},
            }
        ],
    )

    # Return the output of the component
    return save_message_to_file.output


# Example usage
if __name__ == "__main__":
    # Example message and GCS filepath
    message = "Hello, World!"
    gcs_filepath = "gs://my-bucket/sample-file.txt"

    # Call the pipeline function
    result = sample_pipeline(message, gcs_filepath)

    # Print the result
    print(result)
