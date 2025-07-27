import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="HeartDiseasePrediction")
def HeartDiseasePrediction():
    # Load data from a CSV dataset
    load_data = component(
        name="load_data",
        description="Load data from a CSV dataset",
        inputs={
            "url": Input(Dataset("heart_2020_cleaned")),
        },
        outputs={
            "data": Output(Dataset("heart_2020_cleaned")),
        },
        steps=[
            dsl.LoadDataset(input=Input("url")),
        ],
    )

    # Predict heart disease
    predict_heart_disease = component(
        name="predict_heart_disease",
        description="Predict heart disease",
        inputs={
            "data": Input("data"),
        },
        outputs={
            "prediction": Output(Model("heart_disease_prediction")),
        },
        steps=[
            dsl.PredictModel(input=Input("data")),
        ],
    )

    # Combine predictions
    combine_predictions = component(
        name="combine_predictions",
        description="Combine predictions",
        inputs={
            "predictions": Input("prediction"),
        },
        outputs={
            "combined_prediction": Output(Dataset("heart_2020_cleaned")),
        },
        steps=[
            dsl.CombineResults(input=Input("predictions")),
        ],
    )

    # Save combined prediction to a new CSV file
    save_combined_prediction = component(
        name="save_combined_prediction",
        description="Save combined prediction to a new CSV file",
        inputs={
            "combined_prediction": Input("combined_prediction"),
        },
        outputs={
            "output_file": Output(Dataset("heart_2020_cleaned")),
        },
        steps=[
            dsl.SaveDataset(output=Input("output_file")),
        ],
    )

    # Run the pipeline
    pipeline_root = "gs://my-bucket/pipeline-root"
    pipeline = pipeline(
        name="HeartDiseasePrediction",
        steps=[
            load_data,
            predict_heart_disease,
            combine_predictions,
            save_combined_prediction,
        ],
        output_dir=pipeline_root,
        runtime_config={
            "enable_caching": True,
            "retries": 2,
            "resource_limits": {
                "cpu": "1",
                "memory": "1Gi",
            },
        },
    )

    # Compile the pipeline
    kfp.compiler.Compiler().compile(pipeline)
