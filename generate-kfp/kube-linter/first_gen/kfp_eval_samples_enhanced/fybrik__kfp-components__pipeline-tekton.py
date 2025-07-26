import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from kfp.components import get_endpoint, get_result_endpoint


# Define the pipeline
@dsl.pipeline(name="Fybrik housing price estimate pipeline")
def fybrik_housing_price_estimate_pipeline(
    train_dataset_id: str,
    test_dataset_id: str,
    model_name: str,
    model_version: str,
    model_type: str,
    model_hyperparameters: dict,
    result_endpoint: str = None,
):
    # Retrieve endpoints for training and testing datasets
    train_endpoint = get_endpoint(f"{model_name}-training-endpoint")
    test_endpoint = get_endpoint(f"{model_name}-testing-endpoint")

    # Create a result endpoint if not provided
    if result_endpoint is None:
        result_endpoint = get_result_endpoint(f"{model_name}-result-endpoint")

    # Define the training job
    training_job = component(
        "TrainingJob",
        inputs={
            "train_dataset_id": train_dataset_id,
            "test_dataset_id": test_dataset_id,
            "model_name": model_name,
            "model_version": model_version,
            "model_type": model_type,
            "model_hyperparameters": model_hyperparameters,
        },
        outputs={"output": "training-output"},
        steps=[
            component(
                "DataFetchingStep",
                inputs={
                    "endpoint": train_endpoint,
                    "dataset_id": train_dataset_id,
                },
                outputs={"data": "training-data"},
            ),
            component(
                "ModelTrainingStep",
                inputs={
                    "data": "training-data",
                    "model_name": model_name,
                    "model_version": model_version,
                    "model_type": model_type,
                    "model_hyperparameters": model_hyperparameters,
                },
                outputs={"model": "trained-model"},
            ),
            component(
                "ResultSubmissionStep",
                inputs={
                    "model": "trained-model",
                    "result_endpoint": result_endpoint,
                },
                outputs={"submission": "submission"},
            ),
        ],
    )

    # Define the submission job
    submission_job = component(
        "SubmissionJob",
        inputs={
            "model": "trained-model",
            "result_endpoint": result_endpoint,
        },
        outputs={"submission": "submission"},
    )

    # Return the pipeline
    return training_job, submission_job
