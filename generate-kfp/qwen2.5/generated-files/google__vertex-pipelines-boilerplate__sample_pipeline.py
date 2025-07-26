
from kfp import dsl

@dsl.pipeline(name="sample-pipeline")
def sample_pipeline():
    # Define the component `_save_message_to_file`
    @dsl.component
    def _save_message_to_file(message, gcs_filepath):
        # Write the message to GCS
        print(f"Writing message '{message}' to GCS at {gcs_filepath}")
        # Example: Save the message to a file in GCS
        with open(gcs_filepath, 'w') as f:
            f.write(message)

# Example usage of the pipeline
if __name__ == "__main__":
    sample_pipeline()
