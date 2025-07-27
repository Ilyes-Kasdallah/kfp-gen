import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline(
    load_data: Input[Dataset],
    train_model: Input[Model],
    evaluate_model: Input[Model],
    predict_model: Output[Model],
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the diabetes dataset
    load_data = load_data.read_csv(
        "https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv"
    )

    # Train the XGBoost model
    train_model = train_model.fit(load_data)

    # Evaluate the model
    evaluate_model = evaluate_model.predict(load_data)

    # Predict the model
    predict_model = predict_model(train_model)
