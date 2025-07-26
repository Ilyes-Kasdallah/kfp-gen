from kfp import pipeline
from kfp.dsl import component
from kfp.components import KedroRun


@component
def one_pod_pipeline_generator(pipeline_name):
    # Import necessary modules
    from kfp import components
    from kfp.dsl import pipeline
    from kfp.components import KedroRun

    # Define the pipeline
    @pipeline(name=pipeline_name)
    def convert_kedro_pipeline_to_kfp():
        # Define the Kedro pipeline
        kedro_pipeline = components.KedroRun(
            name="my_kedro_pipeline",
            path="path/to/your/kedro/pipeline",
            parameters={"param1": "value1", "param2": "value2"},
        )

        # Execute the Kedro pipeline
        kedro_pipeline.run()


# Example usage
pipeline_name = "convert_kedro_pipeline_to_kfp"
convert_kedro_pipeline_to_kfp()
