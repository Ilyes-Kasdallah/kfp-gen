import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="EmissionPredictionPipeline")
def emission_prediction_pipeline(
    input_data: Dataset[str],
    model: Model[str],
    output_dataset: Dataset[str],
    output_model: Model[str],
    cache_key: str = "cache_key",
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the input data into a dataset
    input_data = Dataset.from_text(input_data)

    # Train the model on the input data
    model = Model.from_pretrained(model)
    model.fit(input_data)

    # Predict emissions for the input data
    emissions = model.predict(input_data)

    # Save the predictions to a dataset
    output_dataset = Dataset.from_text(emissions)

    # Save the model to a dataset
    output_model = Dataset.from_text(model)

    # Cache the model
    model.cache(cache_key)

    # Retry the model if it fails
    for _ in range(retries):
        try:
            model.fit(input_data)
            break
        except Exception as e:
            print(f"Failed to train model: {e}")

    # Return the predictions and model
    return output_dataset, output_model
