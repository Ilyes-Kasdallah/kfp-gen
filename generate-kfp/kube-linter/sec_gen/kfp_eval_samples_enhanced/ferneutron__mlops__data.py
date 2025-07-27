import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="iris_pipeline")
def iris_pipeline(project_id, bq_dataset):
    # Load data from BigQuery
    load_data = component(
        name="load_data",
        description="Load data from BigQuery",
        inputs={
            "project_id": Input(str(project_id)),
            "bq_dataset": Input(str(bq_dataset)),
        },
        outputs={"data": Output(Dataset(type=DatasetType.BIGQUERY))},
        steps=[
            dsl.LoadDataset(
                name="load_dataset",
                dataset_type=DatasetType.BIGQUERY,
                source=f"bigquery://{project_id}/{bq_dataset}",
            )
        ],
    )

    # Train a model
    train_model = component(
        name="train_model",
        description="Train a model",
        inputs={
            "data": Input(Dataset(type=DatasetType.BIGQUERY)),
            "model_type": Input(str("linear")),
        },
        outputs={"model": Output(Model(type=ModelType.LINEAR))},
        steps=[
            dsl.ModelTraining(
                name="train_model",
                model_type=ModelType.LINEAR,
                input_dataset="data",
                output_model="model",
            )
        ],
    )

    # Evaluate the model
    evaluate_model = component(
        name="evaluate_model",
        description="Evaluate the model",
        inputs={
            "model": Input(Model(type=ModelType.LINEAR)),
            "test_dataset": Input(Dataset(type=DatasetType.BIGQUERY)),
        },
        outputs={"metrics": Output(Metrics(type=MetricsType.COUNT))},
        steps=[
            dsl.ModelEvaluation(
                name="evaluate_model",
                model_type=ModelType.LINEAR,
                test_dataset="test_dataset",
                output_metrics="metrics",
            )
        ],
    )

    # Save the model
    save_model = component(
        name="save_model",
        description="Save the model",
        inputs={
            "model": Input(Model(type=ModelType.LINEAR)),
            "output_path": Input(str("gs://my-bucket/model")),
        },
        outputs={"model": Output(Model(type=ModelType.LINEAR))},
        steps=[
            dsl.ModelSaving(
                name="save_model", model_type=ModelType.LINEAR, output_path="model"
            )
        ],
    )

    # Return the pipeline root
    return save_model
