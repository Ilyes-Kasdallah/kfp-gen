
from kubeflow_pipelines import dsl

@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from CSV files
    load_data = dsl.component(
        name="load_data",
        description="Load data from CSV files",
        inputs={
            "data_url": dsl.uri("gs://your-bucket/data.csv"),
            "target_column": dsl.field("target_column_name")
        },
        outputs={
            "features": dsl.field("features"),
            "labels": dsl.field("labels")
        },
        operations=[
            dsl.load_csv(input_uri=dsl.uri("gs://your-bucket/data.csv")),
            dsl.rename_columns(features_column="feature_column_name", target_column="target_column_name"),
            dsl.convert_categorical_column("gender", "gender_mapping")
        ]
    )

    # Train XGBoost model
    train_model = dsl.component(
        name="train_model",
        description="Train XGBoost model",
        inputs={
            "features": dsl.field("features"),
            "labels": dsl.field("labels")
        },
        outputs={
            "model": dsl.field("xgboost_model")
        },
        operations=[
            dsl.xgboost_model(
                input_features=features,
                output_labels=labels,
                num_rounds=50,
                learning_rate=0.01,
                objective="binary:logistic"
            )
        ]
    )

    # Evaluate model
    evaluate_model = dsl.component(
        name="evaluate_model",
        description="Evaluate model",
        inputs={
            "model": dsl.field("xgboost_model"),
            "test_data": dsl.uri("gs://your-bucket/test_data.csv")
        },
        outputs={
            "accuracy": dsl.field("accuracy")
        },
        operations=[
            dsl.evaluate_model(
                input_model=model,
                input_test_data=test_data,
                metric="accuracy"
            )
        ]
    )

    return load_data, train_model, evaluate_model
