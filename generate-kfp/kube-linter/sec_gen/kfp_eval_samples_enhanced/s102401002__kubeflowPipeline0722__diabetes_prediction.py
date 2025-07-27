import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="diabetes_prediction")
def diabetes_prediction(
    load_data: Dataset[Input[Dataset]],
    train_model: Model[Input[Model]],
    predict_model: Model[Output[Model]],
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load data from CSV files
    load_data = load_data.read_csv(
        "https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv"
    )
    load_data = load_data.read_csv(
        "https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv"
    )

    # Train the model
    train_model = train_model.fit(load_data)

    # Predict the model
    predict_model = predict_model.predict(train_model)

    # Cache the model if enabled
    if cache:
        predict_model.cache()

    # Return the predictions
    return predict_model
