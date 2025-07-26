import kfp
from kfp import components
from kfp.dsl import pipeline

# Define the pipeline function name
pipeline_name = "FirstPipeline"


# Define the extract_data component
@components.component(name="extract_data")
def extract_data():
    # Placeholder for extracting data
    print("Extracting data...")
    return "Extracted Data"


# Define the preprocess_data component
@components.component(name="preprocess_data")
def preprocess_data(data):
    # Placeholder for preprocessing data
    print(f"Preprocessing data with {data}")
    return data


# Define the model training component
@components.component(name="model_training")
def model_training(data):
    # Placeholder for model training
    print(f"Training model with {data}")
    return "Model trained"


# Define the pipeline
@pipeline(name=pipeline_name)
def first_pipeline():
    # Extract data
    extracted_data = extract_data()

    # Preprocess data
    preprocessed_data = preprocess_data(extracted_data)

    # Train model
    trained_model = model_training(preprocessed_data)

    return trained_model


# Run the pipeline
if __name__ == "__main__":
    first_pipeline().execute()
