from kfp import pipeline
from kfp.dsl import component

# Define the pipeline function name
pipeline_name = "pipeline-with-env"


@dsl.pipeline(name=pipeline_name)
def pipeline_with_env():
    # Define the first component: print_env_op
    @component
    def print_env_op():
        # Set the ENV1 variable to val1
        env1 = "val1"
        # Print the value of ENV1
        print(f"ENV1: {env1}")
        # Return the printed text
        return f"Printed ENV1: {env1}"

    # Define the second component: print_env_op
    @component
    def print_env_op():
        # Set the ENV2 variable to val2
        env2 = "val2"
        # Print the value of ENV2
        print(f"ENV2: {env2}")
        # Return the printed text
        return f"Printed ENV2: {env2}"

    # Use the components in the pipeline
    print_env_op()
    print_env_op()


# Run the pipeline
if __name__ == "__main__":
    pipeline_with_env()
