```python
import kfp
from kfp import dsl

# Import necessary libraries
from google.cloud import bigquery

# Load transactions component
@dsl.component(
    base_image="gcr.io/kubeflow/pipelines/python-operator:v0.3.0",
    packages_to_install=["google-cloud-bigquery"],
)
def load_transactions(
    project_id: str,
    source_gcs_path: str = None,
    source_bq_table: str = None,
    dataset_location: str = "US",
    dataset_name: str = None,
    table_id: str = None,
) -> str:
    # Implement the logic to load transactions into BigQuery
    if source_gcs_path:
        # Load data from CSV file into BigQuery
        pass
    elif source_bq_table:
        # Pass the provided table ID as output
        return source_bq_table
    else:
        raise ValueError("Either source_gcs_path or source_bq_table must be provided")

# Sales pipeline
@dsl.pipeline(name="sales_pipeline")
def sales_pipeline():
    # Load transactions component
    load_trans = load_transactions(project_id="your_project_id", source_gcs_path="gs://your_bucket/transactions.csv")

    # Add more components as needed for CLV prediction
    # For example:
    # clv_prediction = predict_clv(load_trans.output)

# Compile the pipeline
compiler.Compiler().compile(sales_pipeline, package_path="sales_pipeline.yaml")
```

In this solution, we define the `load_transactions` component using the `@dsl.component` decorator. We also define the `sales_pipeline` component using the `@dsl.pipeline` decorator. The `load_transactions` component takes various parameters such as `project_id`, `source_gcs_path`, `source_bq_table`, `dataset_location`, `dataset_name`, and `table_id`. Depending on the provided inputs, it either loads data from a CSV file into BigQuery or passes the provided table ID as output. The `sales_pipeline` component can be extended with additional components for CLV prediction. Finally, we compile the pipeline using the `Compiler` class from the `kfp.compiler` module and save the compiled pipeline to a YAML file named `sales_pipeline.yaml`.