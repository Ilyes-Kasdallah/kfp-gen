import kfp
from kfp.dsl import pipeline, component


# Define the DAG_Pipeline class
@dsl.pipeline(name="DAG_Pipeline")
def DAG_Pipeline():
    # Define the components
    @component
    def process_data(input_path):
        # Example processing logic
        return f"Processed {input_path}"

    @component
    def transform_data(input_path):
        # Example transformation logic
        return f"Transformed {input_path}"

    @component
    def save_output(output_path):
        # Example saving logic
        return f"Saved {output_path}"

    # Define the dependencies
    dependencies = [process_data, transform_data, save_output]

    # Define the main function
    @component
    def main():
        # Main function to orchestrate the pipeline
        for dependency in dependencies:
            dependency()


# Run the pipeline
if __name__ == "__main__":
    pipeline_manager.run(DAG_Pipeline())
