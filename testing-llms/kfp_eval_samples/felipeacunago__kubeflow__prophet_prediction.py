```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_url

# Load components
bigquery_query_op = load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/bigquery/query/component.yaml')
preprocess_and_split_op = load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/preprocessing/split/component.yaml')
prophet_prediction_and_ranking_op = load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/prophet/predict_and_rank/component.yaml')

# Define the pipeline
@dsl.pipeline(name='Prophet')
def prophet_prediction(
    dataset_query: str,
    val_dataset_query: str,
    split_column: str,
    project_id: str,
    output_gcs_path: str,
    dataset_location: str,
    job_config: dict,
    dictionary_file_path: str,
    minimum_length: int,
    training_date: str,
    changepoint_prior_scale: float,
    evaluation_date: str,
    evaluation_maximum_distance: float,
    predict_periods: int,
    predict_freq: str,
    order_ds: str,
    preprocess_output_path: str,
    val_split_output_path: str,
    predictions_path: str,
    prophet_rank_output_path: str,
    validation_rank_output: str,
    results_output: str
):
    # Step 1: BigQuery Query
    bigquery_query_task = bigquery_query_op(
        dataset_query=dataset_query,
        project_id=project_id,
        output_gcs_path=output_gcs_path,
        dataset_location=dataset_location,
        job_config=job_config
    )

    # Step 2: Preprocess and Split
    preprocess_and_split_task = preprocess_and_split_op(
        original_dataset_path=bigquery_query_task.outputs['output'],
        val_dataset_query=val_dataset_query,
        split_column=split_column,
        preprocess_output_path=preprocess_output_path,
        val_split_output_path=val_split_output_path
    )

    # Step 3: Prophet Prediction and Ranking
    prophet_prediction_and_ranking_task = prophet_prediction_and_ranking_op(
        preprocess_output_path=preprocess_and_split_task.outputs['preprocess_output'],
        val_split_output_path=preprocess_and_split_task.outputs['val_split_output'],
        minimum_length=minimum_length,
        training_date=training_date,
        changepoint_prior_scale=changepoint_prior_scale,
        evaluation_date=evaluation_date,
        evaluation_maximum_distance=evaluation_maximum_distance,
        predict_periods=predict_periods,
        predict_freq=predict_freq,
        order_ds=order_ds,
        predictions_path=predictions_path,
        prophet_rank_output_path=prophet_rank_output_path,
        validation_rank_output=validation_rank_output,
        results_output=results_output
    )
```

This code defines a Kubeflow Pipeline named `Prophet` with three components: `BigQuery Query`, `Preprocess and Split`, and `Prophet Prediction and Ranking`. Each component is defined using the `@dsl.component` decorator, and the pipeline's control flow is sequential. The pipeline uses the `kfp.dsl` and `kfp.components` libraries from Kubeflow Pipelines, along with potentially other libraries within the Docker images used in the components.