
from kfp import pipeline
from kfp.components import component

@dsl.pipeline(name="First Pipeline")
def first_pipeline():
    # Define the extract_data component
    @component
    def extract_data():
        # Placeholder for extracting data
        return "Extracted Data"

    # Define the preprocess_data component
    @component
    def preprocess_data(data):
        # Placeholder for preprocessing data
        return f"Preprocessed Data: {data}"

    # Define the model training component
    @component
    def model_training(data):
        # Placeholder for model training
        return f"Model Trained with Data: {data}"

# Execute the pipeline
first_pipeline()
