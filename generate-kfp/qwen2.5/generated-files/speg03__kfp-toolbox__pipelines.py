
from kfp import pipelines

@dsl.pipeline(name="timestamp-pipeline")
def timestamp_pipeline():
    # Define the timestamp component
    timestamp = (
        pipelines.component(
            name="timestamp",
            python_callable=lambda params: f"{params['year']}-{params['month']}-{params['day']}",
            description="Generates a timestamp string based on provided parameters."
        )
    )

    # Return the timestamp component
    return timestamp
