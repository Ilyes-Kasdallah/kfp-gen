
from kubeflow_pipelines import dsl

@dsl.pipeline(name="DiabetesPredictionPipeline")
def DiabetesPredictionPipeline(nas_mount_path):
    # Load data from NAS
    load_data = dsl.component(
        name="load_data",
        description="Load data from NAS",
        inputs={
            "nas_mount_path": nas_mount_path,
        },
        outputs={
            "artifact": "diabetes_data.csv",
        },
        steps=[
            dsl.load_artifact(
                artifact_name="diabetes_data.csv",
                source="kubernetes://kubeflow_NAS/data/diabetes_data.csv",
            ),
        ],
    )

    # Train a RandomForestClassifier
    train_model = dsl.component(
        name="train_model",
        description="Train a RandomForestClassifier",
        inputs={
            "artifact": "diabetes_data.csv",
        },
        outputs={
            "model": "random_forest_model",
        },
        steps=[
            dsl.random_forest_classifier(
                model_name="random_forest_model",
                input_columns=["feature1", "feature2"],
                output_column="prediction",
            ),
        ],
    )

    # Deploy the trained model
    deploy_model = dsl.component(
        name="deploy_model",
        description="Deploy the trained model",
        inputs={
            "model": "random_forest_model",
        },
        outputs={
            "artifact": "diabetes_prediction_model",
        },
        steps=[
            dsl.deploy_model(
                model_name="diabetes_prediction_model",
                deployment_type="serverless",
                environment_variables={
                    "MODEL_NAME": "random_forest_model",
                },
            ),
        ],
    )

    return load_data, train_model, deploy_model
