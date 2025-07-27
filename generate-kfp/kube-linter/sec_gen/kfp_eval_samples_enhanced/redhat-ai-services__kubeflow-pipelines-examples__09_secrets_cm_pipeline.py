import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="Env Vars Pipeline")
def Env_Vars_Pipeline():
    # Define the first component: print_envvar
    @component(name="print_envvar")
    def print_envvar(env_var):
        # Print the value of the environment variable
        print(f"Environment Variable: {env_var}")

    # Define the second component: get_secret
    @component(name="get_secret")
    def get_secret(secret_name):
        # Retrieve the secret value from a secret manager
        # For this example, we'll assume the secret is stored in a Google Secret Manager
        # Replace 'your-secret-name' with your actual secret name
        secret_value = kfp.components.SecretManager.get_secret_value(
            name=secret_name, project="your-project-id", version="latest"
        )
        return secret_value

    # Define the third component: get_config_map
    @component(name="get_config_map")
    def get_config_map(config_map_name):
        # Retrieve the configuration map value from a configuration map
        # For this example, we'll assume the configuration map is stored in a Google Cloud Config Map
        # Replace 'your-config-map-name' with your actual configuration map name
        config_map_value = kfp.components.ConfigMap.get_config_map_value(
            name=config_map_name, project="your-project-id", version="latest"
        )
        return config_map_value

    # Define the pipeline task: main
    @component(name="main")
    def main():
        # Call the get_secret component to retrieve the secret value
        secret_value = get_secret("your-secret-name")

        # Call the get_config_map component to retrieve the configuration map value
        config_map_value = get_config_map("your-config-map-name")

        # Print the retrieved values
        print(f"Secret Value: {secret_value}")
        print(f"Configuration Map Value: {config_map_value}")


# Compile the pipeline
kfp.compiler.Compiler().compile(Env_Vars_Pipeline)
