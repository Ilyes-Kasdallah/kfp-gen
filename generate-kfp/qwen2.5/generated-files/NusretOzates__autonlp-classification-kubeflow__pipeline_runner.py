
from kfp import pipeline, component

@dsl.pipeline(name="classification_training_pipeline")
def classification_training_pipeline(
    dataset_name: str = "tweet_eval",
    dataset_subset: str = "emotion"
):
    # Define the Data Ingestion Component
    ingest_data = component.Component(
        name="ingest_data",
        description="Ingests data from a specified dataset.",
        inputs={
            "dataset_name": dataset_name,
            "dataset_subset": dataset_subset
        },
        outputs={"data": "pandas.DataFrame"}
    )

    # Define the Text Classification Component
    classify_text = component.Component(
        name="classify_text",
        description="Classifies text data using a pre-trained model.",
        inputs={
            "data": "pandas.DataFrame"
        },
        outputs={"predictions": "pandas.Series"}
    )

    # Define the Pipeline Execution
    with ingest_data:
        data = ingest_data.outputs["data"]

    with classify_text:
        predictions = classify_text.outputs["predictions"]

    # Return the results of the classification
    return predictions
