
from kfp import dsl

@dsl.pipeline(name="Env Vars Pipeline")
def Env_Vars_Pipeline():
    # Define the first component: print_envvar
    @dsl.component(name="print_envvar")
    def print_envvar(env_var):
        # Print the value of the environment variable
        print(f"Value of {env_var}: {os.getenv(env_var)}")

    # Define the second component: get_secret
    @dsl.component(name="get_secret")
    def get_secret(secret_name):
        # Retrieve the secret value from the Kubernetes Secret
        secret = kubernetes.secrets.get(secret_name)
        if secret:
            return secret.data['value']
        else:
            return None

    # Define the third component: get_config_map
    @dsl.component(name="get_config_map")
    def get_config_map(config_map_name):
        # Retrieve the config map value from the Kubernetes ConfigMap
        config_map = kubernetes.configmaps.get(config_map_name)
        if config_map:
            return config_map.data['data']
        else:
            return None

    # Use the components in the pipeline
    print_envvar("MY_ENV_VAR")
    secret_value = get_secret("my-secret")
    config_map_value = get_config_map("my-config-map")

    # Print the results
    print(f"Secret Value: {secret_value}")
    print(f"Config Map Value: {config_map_value}")
