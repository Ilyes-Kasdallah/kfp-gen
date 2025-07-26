from kfp import components
from kfp.dsl import pipeline


@pipeline(name="my_pipeline")
def my_pipeline():
    # Define a simple data processing task
    @components.task(name="process_data")
    def process_data(data):
        # Example processing logic
        processed_data = data * 2
        return processed_data


# Define the after_test function
@pipeline.after_test("my_pipeline")
def after_test():
    print("Pipeline 'my_pipeline' has been executed successfully.")


# Example usage of the pipeline
if __name__ == "__main__":
    my_pipeline()
