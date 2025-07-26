import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Define a component that takes parameters from the pipeline execution
    @component
    def process_data(data):
        # Process the data here
        return data * 2

    # Use the component in the pipeline
    processed_data = process_data("input_data")

    # Return the processed data
    return processed_data


# Example usage
if __name__ == "__main__":
    # Execute the pipeline
    result = my_pipeline()
    print(result)
