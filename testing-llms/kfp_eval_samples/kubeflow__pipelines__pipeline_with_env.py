```python
import kfp
from kfp import dsl

# Define the print_env_op component
@dsl.component(
    base_image='alpine:latest',
    packages_to_install=['bash'],
    outputs=[dsl.Output('output')]
)
def print_env_op():
    # Set the environment variables
    env1 = 'val1'
    env2 = 'val2'
    env3 = 'val3'

    # Print the environment variables
    print(f"ENV1: {env1}")
    print(f"ENV2: {env2}")
    print(f"ENV3: {env3}")

    # Return the output
    return f"Environment variables printed successfully."

# Define the print_env_2_op component
@dsl.component(
    base_image='alpine:latest',
    packages_to_install=['bash'],
    outputs=[dsl.Output('output')]
)
def print_env_2_op(env2):
    # Check if ENV2 is equal to val2
    if env2 == 'val2':
        # Print ENV2 and ENV3
        print(f"ENV2: {env2}")
        print(f"ENV3: {env3}")
    else:
        # Exit with an error
        exit(1)

# Define the pipeline
@dsl.pipeline(name="pipeline-with-env")
def pipeline_with_env():
    # Execute print_env_op
    print_env_op()

    # Execute print_env_2_op with the value of ENV2
    print_env_2_op(dsl.InputValue("ENV2"))

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(pipeline_with_env, "pipeline_with_env.yaml")
```

This code snippet defines a Kubeflow Pipeline named `pipeline-with-env` that includes two components: `print_env_op` and `print_env_2_op`. The `print_env_op` component prints the values of environment variables `ENV1`, `ENV2`, and `ENV3`. The `print_env_2_op` component checks if `ENV2` is equal to `val2` and prints `ENV2` and `ENV3` if true, otherwise exiting with an error. The pipeline's control flow is sequential, with `print_env_op` executing first and then `print_env_2_op` leveraging the environment variables set by the pipeline and its internal environment variable settings.