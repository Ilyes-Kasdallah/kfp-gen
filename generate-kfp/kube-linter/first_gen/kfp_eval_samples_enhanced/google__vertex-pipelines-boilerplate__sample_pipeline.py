from kfp import components
from kfp.dsl import pipeline


@pipeline(name="sample-pipeline")
def sample_pipeline():
    # Define the _save_message_to_file component
    save_message_to_file = components.load_component("path/to/save_message_to_file.py")

    # Define the main function that orchestrates the pipeline
    def main(message, gcs_filepath):
        # Call the _save_message_to_file component with the provided arguments
        save_message_to_file(message, gcs_filepath)


# Example usage of the sample_pipeline function
if __name__ == "__main__":
    sample_pipeline()
