
from kfp import pipeline
from kfp.components import get_component

# Define the pipeline function name
pipeline_function_name = "Fybrik housing price estimate pipeline"

# Define the components
get_data_endpoints = get_component(
    "data-access",
    inputs={
        "train_dataset_id": "string",
        "test_dataset_id": "string"
    },
    outputs={
        "endpoint": "string"
    }
)

# Define the pipeline
@pipeline_function_name
def fybrik_housing_price_estimate_pipeline(
    train_dataset_id: str,
    test_dataset_id: str
):
    # Retrieve endpoints for training and testing datasets
    endpoint_train = get_data_endpoints(train_dataset_id)
    endpoint_test = get_data_endpoints(test_dataset_id)
    
    # Define the model training component
    model_training = get_component(
        "model-training",
        inputs={
            "endpoint": endpoint_train
        },
        outputs={
            "model": "string"
        }
    )
    
    # Define the result submission component
    result_submission = get_component(
        "result-submission",
        inputs={
            "model": "string",
            "output_file_path": "string"
        },
        outputs={
            "submission_url": "string"
        }
    )
    
    # Return the pipeline
    return {
        "endpoint_train": endpoint_train,
        "endpoint_test": endpoint_test,
        "model_training": model_training,
        "result_submission": result_submission
    }
