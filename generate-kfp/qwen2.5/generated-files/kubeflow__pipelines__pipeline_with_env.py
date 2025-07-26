
from kfp import dsl

@dsl.pipeline(name="pipeline-with-env")
def pipeline_with_env():
    # Define the components
    print_env_op = dsl.component(
        name="print_env_op",
        description="Prints the values of environment variables ENV1 and ENV2.",
        steps=[
            dsl.output("env1", type=str),
            dsl.output("env2", type=str)
        ],
        env_vars={
            "ENV1": "val1",
            "ENV2": "val2"
        }
    )

    # Execute the pipeline
    print_env_op()
