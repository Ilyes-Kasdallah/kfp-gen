import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Stroke Prediction Pipeline")
def stroke_prediction():
    # Load data from two CSV files
    load_data = component(
        name="load_data",
        description="Load stroke prediction data from two CSV files.",
        inputs={
            "file1": Input(
                Dataset(
                    "https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/stroke.csv"
                )
            ),
            "file2": Input(
                Dataset(
                    "https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/stroke.csv"
                )
            ),
        },
        outputs={"data": Output(Dataset("stroke_data"))},
    )

    # Perform preprocessing on the loaded data
    preprocess_data = component(
        name="preprocess_data",
        description="Preprocess the stroke prediction data.",
        inputs={"data": Input(Dataset("stroke_data"))},
        outputs={"cleaned_data": Output(Dataset("cleaned_data"))},
    )

    # Train a machine learning model
    train_model = component(
        name="train_model",
        description="Train a machine learning model.",
        inputs={"cleaned_data": Input(Dataset("cleaned_data"))},
        outputs={"model": Output(Model("model"))},
    )

    # Make predictions on the cleaned data
    predict_model = component(
        name="predict_model",
        description="Make predictions on the cleaned data.",
        inputs={
            "model": Input(Model("model")),
            "cleaned_data": Input(Dataset("cleaned_data")),
        },
        outputs={"predictions": Output(Dataset("predictions"))},
    )

    # Save the predictions to a new dataset
    save_predictions = component(
        name="save_predictions",
        description="Save the predictions to a new dataset.",
        inputs={"predictions": Input(Dataset("predictions"))},
        outputs={"predictions_dataset": Output(Dataset("predictions_dataset"))},
    )

    # Return the predictions dataset
    return save_predictions()


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiler = kfp.compiler.Compiler()
compiler.compile(stroke_prediction(), pipeline_root)
