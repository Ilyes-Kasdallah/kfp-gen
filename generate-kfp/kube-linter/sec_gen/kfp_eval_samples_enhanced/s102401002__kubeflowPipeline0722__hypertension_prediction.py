import pandas as pd
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="HypertensionPredictionPipeline")
def hypertension_prediction():
    # Load data from CSV file
    load_data = component(
        name="loadData",
        description="Load hypertension data from a CSV file",
        inputs={
            "csv_file": Input(
                Dataset(
                    "https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/hypertension_data.csv"
                )
            )
        },
        outputs={"data": Output(Dataset("hypertension_data"))},
    )

    # Process the data
    process_data = component(
        name="processData",
        description="Process the loaded data",
        inputs={"data": Input(Dataset("hypertension_data"))},
        outputs={"processed_data": Output(Dataset("processed_data"))},
    )

    # Predict hypertension
    predict_hypertension = component(
        name="predictHypertension",
        description="Predict hypertension based on processed data",
        inputs={"processed_data": Input(Dataset("processed_data"))},
        outputs={"prediction": Output(Model("hypertension_prediction"))},
    )

    # Save the prediction
    save_prediction = component(
        name="savePrediction",
        description="Save the prediction to a model",
        inputs={"prediction": Input(Model("hypertension_prediction"))},
        outputs={"model": Output(Model("hypertension_model"))},
    )

    # Return the pipeline root
    return save_prediction


# Example usage of the pipeline function
if __name__ == "__main__":
    pipeline_root = "gs://my-bucket/pipeline-root"
    pipeline(hypertension_prediction)
