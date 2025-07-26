
from kubeflow_pipelines import dsl

@dsl.pipeline(name="convert_kedro_pipeline_to_kfp")
def convert_kedro_pipeline_to_kfp(pipeline_name):
    # Define the component that executes the Kedro pipeline
    @dsl.component
    def execute_kedro_pipeline(pipeline_name):
        # Execute the Kedro pipeline using the 'kedro run' command
        return f"kedro run {pipeline_name}"

    # Return the component
    return execute_kedro_pipeline
