import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="taxi-on-prem")
def taxi_on_prem(
    inference_data: Dataset,
    validation_data: Dataset,
    column_names: list[str],
    key_columns: list[str],
    project: str,
    mode: str,
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Define the data validation operation
    dataflow_tf_data_validation_op = component(
        name="dataflow_tf_data_validation_op",
        description="Runs TensorFlow Data Validation on the provided data.",
        inputs={
            "inference_data": inference_data,
            "validation_data": validation_data,
            "column_names": column_names,
            "key_columns": key_columns,
            "project": project,
            "mode": mode,
        },
        outputs={"/schema": Output(Dataset)},
        steps=[
            dsl.TfDataValidation(
                input=dataset,
                output=dataset,
                column_names=column_names,
                key_columns=key_columns,
                project=project,
                mode=mode,
                cache=cache,
                retries=retries,
                resource_limits=resource_limits,
            )
        ],
    )

    # Define the main pipeline task
    main_pipeline_task = component(
        name="main_pipeline_task",
        description="Runs the main pipeline logic.",
        inputs={"dataflow_tf_data_validation_op": dataflow_tf_data_validation_op},
        outputs={"predictions": Output(Dataset)},
        steps=[
            dsl.Predictions(
                input=dataflow_tf_data_validation_op.outputs["/schema"],
                output=dataset,
                model=Model.from_gcs("gs://my-bucket/taxi-model"),
                metrics=Metrics("accuracy", "precision", "recall", "f1-score"),
            )
        ],
    )

    # Return the main pipeline task
    return main_pipeline_task
