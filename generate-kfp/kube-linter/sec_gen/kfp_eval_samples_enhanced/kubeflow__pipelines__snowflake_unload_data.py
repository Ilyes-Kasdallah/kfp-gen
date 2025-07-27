import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the Snowflake Unload Operation component
@component
def snowflake_unload_op(
    snowflake_conn_id: str,
    source_table: str,
    destination_bucket: str,
    output_dataset: Dataset,
    output_model: Model,
    max_retries: int = 2,
    cache: bool = True,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load data from Snowflake
    load_task = dsl.Load(
        data_source=snowflake_conn_id, table=source_table, output=output_dataset
    )

    # Unload data to GCS
    unload_task = dsl.Unload(
        data_source=output_dataset,
        output=output_model,
        bucket=destination_bucket,
        max_retries=max_retries,
        cache=cache,
        resource_limits=resource_limits,
    )

    return load_task, unload_task


# Define the pipeline
@pipeline(name="snowflake_data_unload")
def snowflake_data_unload():
    # Call the Snowflake Unload Operation component
    load_task, unload_task = snowflake_unload_op(
        snowflake_conn_id="your-snowflake-connection-id",
        source_table="your-source-table",
        destination_bucket="your-destination-bucket",
        output_dataset="your-output-dataset",
        output_model="your-output-model",
        max_retries=2,
        cache=True,
        resource_limits={"cpu": "1", "memory": "1Gi"},
    )

    # Print the results of the operations
    print("Load Task Results:")
    print(load_task.output)
    print("\nUnload Task Results:")
    print(unload_task.output)


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(snowflake_data_unload)
