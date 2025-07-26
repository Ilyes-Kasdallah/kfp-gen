from kfp import pipeline
from kfp.dsl import component


@component
def print_envvar(env_var: str) -> None:
    """Prints the value of an environment variable."""
    print(f"The value of {env_var} is: {env_var}")


@pipeline(name="Env Vars Pipeline")
def env_vars_pipeline():
    """Runs two tasks to demonstrate accessing secrets and config maps."""
    # Task 1: Print the value of an environment variable
    print_envvar("MY_ENV_VAR")

    # Task 2: Print the value of a secret from a ConfigMap
    secret_name = "my-secret"
    secret_value = kfp.components.get_secret(secret_name)
    print_envvar(secret_value)


# Run the pipeline
env_vars_pipeline()
