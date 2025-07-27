import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="crypto_pipeline")
def crypto_pipeline(target_bucket):
    # Define the raw_data_transfer component
    @component
    def raw_data_transfer(input_dataset, target_bucket):
        # Transfer the raw dataset to GCS
        return f"gs://{target_bucket}/output.txt"

    # Define the model_training component
    @component
    def model_training(input_dataset, model_name):
        # Train a model on the dataset
        return f"{model_name}.model"

    # Define the model_prediction component
    @component
    def model_prediction(input_model, input_dataset):
        # Predict the closing price of the Bitcoin
        return f"{input_model}.prediction"

    # Define the pipeline task
    @dsl.task(name="predict_close_price")
    def predict_close_price(input_dataset, model_name):
        # Call the model training and prediction components
        model_output = model_training(input_dataset, model_name)
        prediction_output = model_prediction(model_output, input_dataset)
        return prediction_output


# Define the pipeline root parameter
pipeline_root = "gs://my-bucket/pipeline-root"

# Compile the pipeline
kfp.compiler.Compiler().compile(crypto_pipeline, pipeline_root)
