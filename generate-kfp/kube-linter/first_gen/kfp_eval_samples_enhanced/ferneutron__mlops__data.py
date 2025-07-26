import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from google.cloud import bigquery
from google.cloud import storage


# Define the pipeline
@pipeline(name="iris_pipeline")
def iris_pipeline(project_id, bq_dataset):
    # Load data from BigQuery
    load_data = component(
        name="load_data",
        description="Load data from BigQuery",
        inputs={
            "project_id": kfp.dsl.Input("project_id", type=str),
            "bq_dataset": kfp.dsl.Input("bq_dataset", type=str),
        },
        outputs={"data": kfp.dsl.Output("data", type=bigquery.Table)},
        steps=[
            component(
                name="read_data",
                description="Read data from BigQuery",
                inputs={"table": kfp.dsl.Input("table", type=bigquery.Table)},
                outputs={"data": kfp.dsl.Output("data", type=bigquery.Table)},
            ),
            component(
                name="transform_data",
                description="Transform data",
                inputs={"data": kfp.dsl.Input("data", type=bigquery.Table)},
                outputs={
                    "transformed_data": kfp.dsl.Output(
                        "transformed_data", type=bigquery.Table
                    )
                },
            ),
        ],
    )

    # Save transformed data to Google Cloud Storage
    save_data = component(
        name="save_data",
        description="Save transformed data to Google Cloud Storage",
        inputs={
            "transformed_data": kfp.dsl.Input("transformed_data", type=bigquery.Table)
        },
        outputs={"storage_path": kfp.dsl.Output("storage_path", type=str)},
        steps=[
            component(
                name="upload_to_storage",
                description="Upload transformed data to Google Cloud Storage",
                inputs={
                    "storage_path": kfp.dsl.Input("storage_path", type=str),
                    "table": kfp.dsl.Input("table", type=bigquery.Table),
                },
                outputs={"storage_path": kfp.dsl.Output("storage_path", type=str)},
            )
        ],
    )

    # Return the storage path of the transformed data
    return save_data.outputs["storage_path"]
