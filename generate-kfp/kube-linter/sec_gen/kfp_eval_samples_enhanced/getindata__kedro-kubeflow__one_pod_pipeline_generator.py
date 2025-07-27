import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="convert_kedro_pipeline_to_kfp")
def convert_kedro_pipeline_to_kfp(kedro_pipeline_name):
    # Define the component
    @component
    def execute_kedro_pipeline(kedro_pipeline_name):
        # Execute the Kedro pipeline using the kedro run command
        result = kfp.run(
            pipeline_name=kedro_pipeline_name,
            parameters={"output_dir": "gs://my-bucket/output", "log_level": "INFO"},
        )
        return result

    # Return the component
    return execute_kedro_pipeline


# Example usage
if __name__ == "__main__":
    # Define the pipeline name
    pipeline_name = "example-pipeline"

    # Execute the pipeline
    result = convert_kedro_pipeline_to_kfp(pipeline_name)
    print(result)
