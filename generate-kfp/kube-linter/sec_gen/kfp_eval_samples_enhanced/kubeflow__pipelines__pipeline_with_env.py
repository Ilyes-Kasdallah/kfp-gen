import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline with an environment variable check
@dsl.pipeline(name="pipeline-with-env")
def pipeline_with_env():
    # Define the first component: print_env_op
    @component
    def print_env_op():
        # Print the values of environment variables ENV1 and ENV2
        print(f"ENV1: {kfp.env.ENV1}, ENV2: {kfp.env.ENV2}")

    # Define the second component: print_env_op
    @component
    def print_env_op():
        # Print the values of environment variables ENV1 and ENV2
        print(f"ENV1: {kfp.env.ENV1}, ENV2: {kfp.env.ENV2}")

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Execute the pipeline
    pipeline(steps=[print_env_op(), print_env_op()], pipeline_root=pipeline_root)
