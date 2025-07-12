```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
read_metadata = load_component_from_file('/path/to/components/read_metadata.yaml')
bq2tfrecord = load_component_from_file('/path/to/components/bq2tfrecord.yaml')
validate_data = load_component_from_file('/path/to/components/validate_data.yaml')
train_nn = load_component_from_file('/path/to/components/train_nn.yaml')
deploy_nn = load_component_from_file('/path/to/components/deploy_nn.yaml')
make_predictions = load_component_from_file('/path/to/components/make_predictions.yaml')
plot_time_series = load_component_from_file('/path/to/components/plot_time_series.yaml')

# Define the pipeline
@dsl.pipeline(name='Time-Series-Forecast for Chicago Taxi dataset')
def build_pipeline(
    artifacts_dir: str,
    model_dir: str,
    project_id: str,
    start_date: str,
    end_date: str,
    split_date: str,
    window_size: int,
    model_name: str,
    deployed_model_name: str,
    dataflow_runner: str,
    epochs: int,
    train_batch_size: int,
    prediction_batch_size: int,
    gpu_mem_usage: float
):
    # Read metadata
    read_metadata_op = read_metadata(project_id=project_id, start_date=start_date, end_date=end_date, split_date=split_date, artifacts_dir=artifacts_dir)

    # Extract and transform data
    bq2tfrecord_op = bq2tfrecord(artifacts_dir=artifacts_dir, project_id=project_id, window_size=window_size, start_date=start_date, end_date=end_date, split_date=split_date)

    # Validate data
    validate_data_op = validate_data(artifacts_dir=artifacts_dir)

    # Train NN
    train_nn_op = train_nn(artifacts_dir=artifacts_dir, model_dir=model_dir, project_id=project_id, start_date=start_date, end_date=end_date, split_date=split_date, window_size=window_size, model_name=model_name, epochs=epochs, train_batch_size=train_batch_size, prediction_batch_size=prediction_batch_size, gpu_mem_usage=gpu_mem_usage)

    # Deploy NN
    deploy_nn_op = deploy_nn(model_dir=model_dir, project_id=project_id, model_name=model_name, deployed_model_name=deployed_model_name, dataflow_runner=dataflow_runner)

    # Make predictions
    make_predictions_op = make_predictions(deployed_model_name=deployed_model_name)

    # Plot time series
    plot_time_series_op = plot_time_series(make_predictions_op.outputs['predictions'])

# Execute the pipeline
if __name__ == '__main__':
    from kfp.compiler import.Compiler
    compiler = Compiler()
    pipeline_spec = compiler.compile(build_pipeline, package_path='time_series_forecast_pipeline.json')
    client = kfp.Client()
    client.create_run_from_pipeline_package(pipeline_spec=pipeline_spec)
```

This code defines a Kubeflow Pipeline named `Time-Series-Forecast for Chicago Taxi dataset` with seven components, each performing specific tasks related to time series forecasting on the Chicago Taxi dataset. The pipeline uses the Kubeflow Pipelines SDK and includes dependencies between components based on their functionality.