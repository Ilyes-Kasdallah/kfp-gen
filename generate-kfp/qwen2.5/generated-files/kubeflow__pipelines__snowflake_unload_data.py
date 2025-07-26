
from kfp import dsl

@dsl.pipeline(name="snowflake_data_unload")
def snowflake_data_unload():
    # Define the Snowflake connection
    snowflake_conn = dsl.Connection(
        project="your-project-id",
        region="your-region",
        database="your-database-name",
        schema="your-schema-name"
    )

    # Define the GCS connection
    gcs_conn = dsl.Connection(
        project="your-project-id",
        region="your-region",
        bucket="your-bucket-name"
    )

    # Define the Snowflake unload operation
    snowflake_unload_op = dsl.component(
        name="snowflake_unload_op",
        description="Unloads data from Snowflake to GCS",
        inputs={
            "snowflake_conn": snowflake_conn,
            "gcs_conn": gcs_conn
        },
        outputs={
            "unloaded_data": dsl.Output("unloaded_data")
        },
        steps=[
            dsl.task(
                name="fetch_data",
                description="Fetches data from Snowflake",
                inputs={
                    "snowflake_conn": snowflake_conn
                },
                outputs={
                    "data": dsl.Output("data")
                },
                steps=[
                    dsl.snowflake_query(
                        query="SELECT * FROM your_table_name",
                        conn=snowflake_conn
                    )
                ]
            ),
            dsl.task(
                name="upload_to_gcs",
                description="Uploads data to GCS",
                inputs={
                    "data": dsl.Input("unloaded_data"),
                    "gcs_conn": gcs_conn
                },
                outputs={
                    "uploaded_data": dsl.Output("uploaded_data")
                },
                steps=[
                    dsl.gcs_upload(
                        file_path="data.csv",
                        bucket=gcs_conn.bucket,
                        object_name="your-object-name"
                    )
                ]
            )
        ]
    )

    return snowflake_unload_op
