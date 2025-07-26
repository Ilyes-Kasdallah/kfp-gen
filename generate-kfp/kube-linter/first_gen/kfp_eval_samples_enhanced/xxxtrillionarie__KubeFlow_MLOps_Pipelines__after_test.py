from kfp import pipeline
from kfp.dsl import component


@component
def after_test():
    # Placeholder for the logic to be executed after the test
    print("Executing after_test component")


@pipeline(name="my_pipeline")
def my_pipeline():
    # First component: does nothing
    @component
    def process_data():
        print("Processing data")
        return "Processed data"

    # Second component: trains a model
    @component
    def train_model(data):
        print("Training model")
        return "Model trained"

    # Combine the two components into a single pipeline
    return process_data() | train_model()


# Run the pipeline
my_pipeline()
