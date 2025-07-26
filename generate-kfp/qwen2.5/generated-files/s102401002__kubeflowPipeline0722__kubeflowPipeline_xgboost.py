
from kubeflow_pipelines import dsl

@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from two URLs
    load_data = dsl.component(
        name="load_data",
        task_type="load_data",
        source=[
            dsl.uri("https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv"),
            dsl.uri("https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv")
        ],
        destination="data"
    )

    # Train XGBoost model
    train_model = dsl.component(
        name="train_model",
        task_type="train_model",
        source=["data"],
        model_type="xgboost",
        hyperparameters={
            "objective": "binary:logistic",
            "max_depth": 3,
            "learning_rate": 0.01,
            "n_estimators": 100
        },
        destination="model"
    )

    # Evaluate the model
    evaluate_model = dsl.component(
        name="evaluate_model",
        task_type="evaluate_model",
        source=["model"],
        metric="accuracy",
        destination="evaluation"
    )

# Run the pipeline
diabetes_prediction_pipeline()
