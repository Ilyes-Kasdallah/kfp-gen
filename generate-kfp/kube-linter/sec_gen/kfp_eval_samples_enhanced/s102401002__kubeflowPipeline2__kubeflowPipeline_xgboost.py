import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline(
    load_data: Input[Dataset],
    train_data: Input[Dataset],
    test_data: Input[Dataset],
    model: Model,
    predictions: Output[Dataset],
    metrics: Output[Metrics],
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load data from CSV files
    load_data = load_data.read_csv("path/to/data.csv")
    train_data = train_data.read_csv("path/to/train.csv")
    test_data = test_data.read_csv("path/to/test.csv")

    # Handle missing values and perform data cleaning
    load_data = load_data.dropna(subset=["age", "sex", "bmi"])
    train_data = train_data.dropna(subset=["age", "sex", "bmi"])
    test_data = test_data.dropna(subset=["age", "sex", "bmi"])

    # Rename columns based on a mapping
    load_data = load_data.rename(columns={"age": "age", "sex": "gender", "bmi": "bmi"})
    train_data = train_data.rename(
        columns={"age": "age", "sex": "gender", "bmi": "bmi"}
    )
    test_data = test_data.rename(columns={"age": "age", "sex": "gender", "bmi": "bmi"})

    # Convert categorical data to numerical representations
    load_data = load_data.replace({"male": 0, "female": 1})
    train_data = train_data.replace({"male": 0, "female": 1})
    test_data = test_data.replace({"male": 0, "female": 1})

    # Split data into training and testing sets
    train_data = train_data.sample(frac=0.8, random_state=42)
    test_data = test_data.sample(frac=0.2, random_state=42)

    # Train the XGBoost model
    model = xgboost.train(
        input_fn=lambda x: x.to_numpy(),
        model_fn=lambda x: x,
        params={
            "objective": "binary:logistic",
            "learning_rate": 0.01,
            "max_depth": 3,
            "min_samples_split": 2,
            "n_estimators": 1000,
            "cache_dir": cache,
            "retries": retries,
            "resource_limits": resource_limits,
        },
        train_dataset=train_data,
        eval_dataset=test_data,
    )

    # Make predictions
    predictions = model.predict(test_data)

    # Calculate metrics
    metrics = model.evaluate(test_data, predictions)

    return predictions, metrics
