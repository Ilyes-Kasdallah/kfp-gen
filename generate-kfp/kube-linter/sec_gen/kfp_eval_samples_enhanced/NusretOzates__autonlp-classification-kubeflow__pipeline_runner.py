import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="classification_training_pipeline")
def classification_training_pipeline(
    dataset_name: str = "tweet_eval",
    dataset_subset: str = "emotion",
    # Add more parameters as needed
):
    # Data ingestion component
    ingest_data = component(
        name="ingest_data",
        description="Ingests data from a specified dataset.",
        inputs={
            "dataset_name": Input(str(dataset_name)),
            "dataset_subset": Input(str(dataset_subset)),
        },
        outputs={"data": Output(Dataset())},
    )

    # Text classification component
    classify_text = component(
        name="classify_text",
        description="Classifies text based on the provided dataset.",
        inputs={"data": Input(Dataset())},
        outputs={"model": Output(Model())},
    )

    # Pipeline execution
    pipeline_execution = pipeline(
        name="classification_training_pipeline", steps=[ingest_data, classify_text]
    )

    # Run the pipeline
    pipeline_execution.run()
