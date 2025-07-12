```python
import os
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from files
print_envvar_op = load_component_from_file('components/print_envvar.yaml')
use_secret_as_env_op = load_component_from_file('components/use_secret_as_env.yaml')
use_config_map_as_env_op = load_component_from_file('components/use_config_map_as_env.yaml')

# Define the pipeline
@dsl.pipeline(name='Env Vars Pipeline')
def env_vars_pipeline(env_var):
    # Print the environment variable
    print_envvar_task = print_envvar_op(env_var=env_var)
    
    # Inject secret into environment
    use_secret_as_env_task = use_secret_as_env_op(
        secret_name='my-secret',
        env_var_name='my-secret-env-var'
    )
    
    # Inject config map into environment
    use_config_map_as_env_task = use_config_map_as_env_op(
        config_map_name='my-configmap',
        env_var_name='my-cm-env-var'
    )

# Execute the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(env_vars_pipeline, '09_secrets_cm_pipeline.py')
```

This code snippet defines a Kubeflow Pipeline named `Env Vars Pipeline` that includes two components: `print_envvar` and `use_secret_as_env`. The `print_envvar` component prints the value of an environment variable, while the `use_secret_as_env` component injects a secret into the environment of the first component. The pipeline uses the `os` module and the Kubeflow SDK (`kfp.dsl`, `kfp.kubernetes`) for pipeline definition and secret/config map injection. The pipeline does not use any machine learning libraries such as `sklearn` or data processing libraries such as `Snowflake`. The pipeline relies on pre-existing Kubernetes secrets (`my-secret`) and config maps (`my-configmap`). The pipeline also uses environment variables `KUBEFLOW_ENDPOINT` and `BEARER_TOKEN` for connecting to the Kubeflow cluster.