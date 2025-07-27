import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the legacy_exit_handler function
@component
def legacy_exit_handler(
    input_file: Input[Dataset],
    output_file: Output[Model],
    cache_key: Output[str],
    retries: Output[int],
    resource_limits: Output[dict],
    legacy_exit_handler: Output[bool],
):
    # Download the file from GCS
    gsutil_command = f"gsutil cp {input_file.uri} {output_file.uri}"
    # Execute the command using the legacy_exit_handler
    legacy_exit_handler.execute(command=gsutil_command)
    # Cache the file
    cache_key.set_value(output_file.uri)
    # Set retries
    retries.set_value(retries.value + 1)
    # Set resource limits
    resource_limits.set_value({"cpu": "1", "memory": "1Gi"})
    # Return True if the legacy_exit_handler was successful
    legacy_exit_handler.set_value(True)


# Define the pipeline
@pipeline(name="Exit Handler")
def exit_handler_pipeline(
    input_file: Input[Dataset],
    output_file: Output[Model],
    cache_key: Output[str],
    retries: Output[int],
    resource_limits: Output[dict],
    legacy_exit_handler: Output[bool],
):
    # Call the legacy_exit_handler function
    legacy_exit_handler()


# Compile the pipeline
exit_handler_pipeline.compile()
