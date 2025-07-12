```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the snowflake_unload component
snowflake_unload = load_component_from_file('components/snowflake_unload.yaml')

# Define the pipeline
@dsl.pipeline(name='snowflake_data_unload')
def snowflake_data_unload(
    output_gcs_path: str,
    sf_storage_integration: str,
    query: str,
    sf_user: str,
    sf_password: str,
    sf_account: str,
    sf_warehouse: str,
    sf_database: str
):
    # Execute the snowflake_unload component
    snowflake_unload_op = snowflake_unload(
        output_gcs_path=output_gcs_path,
        sf_storage_integration=sf_storage_integration,
        query=query,
        sf_user=sf_user,
        sf_password=sf_password,
        sf_account=sf_account,
        sf_warehouse=sf_warehouse,
        sf_database=sf_database
    )
```

This code defines a Kubeflow Pipeline named `snowflake_data_unload` that uses the `snowflake_unload` component to unload data from a Snowflake database to a Google Cloud Storage (GCS) bucket. The pipeline consists of one component: `snowflake_unload_op`, which takes several parameters such as the GCS path, Snowflake storage integration, SQL query, and credentials. The pipeline executes the `snowflake_unload_op` component once and returns a string representing the full GCS path of the unloaded CSV file.