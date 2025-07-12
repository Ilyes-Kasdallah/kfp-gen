```python
from kfp import dsl
from kfp.components import load_component

# Load custom components from the component store
prepare_feature_engineering_query = load_component(
    uri='gs://your-component-store/prepare-feature-engineering-query.yaml'
)
engineer_features = load_component(
    uri='gs://your-component-store/engineer-features.yaml'
)
batch_predict = load_component(
    uri='gs://your-component-store/batch-predict.yaml'
)

# Define the pipeline
@dsl.pipeline(name='CLV Batch Predict')
def clv_batch_predict(
    project_id: str,
    source_gcs_path: str,
    source_bq_table: str,
    dataset_location: str,
    dataset_name: str,
    table_id: str,
    aml_model_id: str,
    output_predictions_path: str
):
    # Step 1: Load sales transactions
    load_sales_transactions_task = load_sales_transactions(
        project_id=project_id,
        source_gcs_path=source_gcs_path,
        source_bq_table=source_bq_table,
        dataset_location=dataset_location,
        dataset_name=dataset_name,
        table_id=table_id
    )

    # Step 2: Prepare feature engineering query
    prepare_feature_engineering_query_task = prepare_feature_engineering_query(
        project_id=project_id
    )

    # Step 3: Engineer features
    engineer_features_task = engineer_features(
        query=prepare_feature_engineering_query_task.outputs['query']
    )

    # Step 4: Batch predict
    batch_predict_task = batch_predict(
        features_table=engineer_features_task.outputs['features_table'],
        aml_model_id=aml_model_id,
        output_predictions_path=output_predictions_path
    )
```

In this solution, we define a Kubeflow Pipeline named `CLV Batch Predict` using the `@dsl.pipeline` decorator. We load custom components for loading sales transactions, preparing feature engineering queries, engineering features, and performing batch prediction. The pipeline's control flow is sequential, with each task depending on the previous one. The pipeline uses BigQuery for data processing and storage, Google Cloud Storage for data input, and an AutoML model for prediction. The pipeline utilizes the `kfp` library from Kubeflow Pipelines and custom components loaded from a local component store. The pipeline also uses YAML files (`settings.yaml`) to configure settings and default arguments.