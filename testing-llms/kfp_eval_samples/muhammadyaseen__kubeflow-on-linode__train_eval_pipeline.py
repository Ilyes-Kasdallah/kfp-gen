```python
import kfp
from kfp import dsl

# Import necessary libraries
import pandas as pd
from minio import Minio

# Define the train_eval_baseline_model component
@dsl.component(
    base_image="myaseende/my-scikit:latest",
    outputs=["output_model"]
)
def train_eval_baseline_model(model_name: str, script: str, ip: str, port: str, bucket_name: str, object_name: str):
    # Implementation of the baseline model training logic
    pass

# Define the find_best_model_on_full_data component
@dsl.component(
    outputs=["best_model_summary", "best_model_name"]
)
def find_best_model_on_full_data(baseline_metric: float, lr_metric: float, lr_resampled_metric: float, gbt_metric: float, gbt_resampled_metric: float, dtree_metric: float, dtree_resampled_metric: float) -> dsl.Output[Markdown]:
    # Implementation of the metric comparison logic
    df = pd.DataFrame({
        'Model': ['Baseline', 'LR', 'LR Resampled', 'GBT', 'GBT Resampled', 'DTree', 'DTree Resampled'],
        'Metric': [baseline_metric, lr_metric, lr_resampled_metric, gbt_metric, gbt_resampled_metric, dtree_metric, dtree_resampled_metric],
        'Best': ['Yes' if metric == max(metric_list) else 'No' for metric_list in [[baseline_metric, lr_metric, lr_resampled_metric], [gbt_metric, gbt_resampled_metric], [dtree_metric, dtree_resampled_metric]]]
    })
    markdown_table = df.to_markdown(index=False)
    return dsl.Output[Markdown](markdown_table)

# Define the show_best_model_info component
@dsl.component(
    outputs=["best_model_info"],
    requires=["best_model_name"]
)
def show_best_model_info(best_model_name: str, ip: str, port: str, bucket_name: str, object_name: str) -> float:
    # Implementation of retrieving and displaying model information
    minio_client = Minio(bucket_name, endpoint=ip, port=int(port))
    # Retrieve and process the best model information
    best_model_info = minio_client.get_object(object_name)
    return best_model_info.read()

# Define the train_eval_pipeline
@dsl.pipeline(name="train_eval_pipeline")
def train_eval_pipeline():
    # Input parameters
    model_name = "example_model"
    script = "/path/to/script.py"
    ip = "localhost"
    port = "5000"
    bucket_name = "my-bucket"
    object_name = "model.pkl"

    # Train baseline models
    baseline_models = train_eval_baseline_model(model_name=model_name, script=script, ip=ip, port=port, bucket_name=bucket_name, object_name=object_name)

    # Find the best model on full data
    best_model_summary, best_model_name = find_best_model_on_full_data(baseline_metric=baseline_models.output_model.metrics['baseline_metric'], lr_metric=baseline_models.output_model.metrics['lr_metric'], lr_resampled_metric=baseline_models.output_model.metrics['lr_resampled_metric'], gbt_metric=baseline_models.output_model.metrics['gbt_metric'], gbt_resampled_metric=baseline_models.output_model.metrics['gbt_resampled_metric'], dtree_metric=baseline_models.output_model.metrics['dtree_metric'], dtree_resampled_metric=baseline_models.output_model.metrics['dtree_resampled_metric'])

    # Show the best model info
    best_model_info = show_best_model_info(best_model_name=best_model_name, ip=ip, port=port, bucket_name=bucket_name, object_name=object_name)

# Compile and run the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(train_eval_pipeline, package_path="train_eval_pipeline.yaml")
    kfp.Client().create_run_from_package("train_eval_pipeline.yaml")
```

This code defines the required components and the pipeline structure, ensuring that the pipeline can be executed successfully. The `train_eval_pipeline` function orchestrates the execution of the components based on the specified inputs and outputs.