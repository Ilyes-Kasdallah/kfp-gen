```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_url

# Load components
download_dataset_op = load_component_from_url('https://raw.githubusercontent.com/drobnov1994/example-kubeflow/master/components/download_dataset.yaml')
train_model_op = load_component_from_url('https://raw.githubusercontent.com/drobnov1994/example-kubeflow/master/components/train_model.yaml')
evaluate_model_op = load_component_from_url('https://raw.githubusercontent.com/drobnov1994/example-kubeflow/master/components/evaluate_model.yaml')
export_model_op = load_component_from_url('https://raw.githubusercontent.com/drobnov1994/example-kubeflow/master/components/export_model.yaml')

# Define the pipeline
@dsl.pipeline(name='End-to-End MNIST Pipeline', description='A pipeline for end-to-end machine learning tasks.')
def end_to_end_mnist_pipeline(
    input_bucket='pipelines-tutorial-data',
    dataset_name='mnist',
    export_bucket='models',
    model_name='mnist',
    model_version='1'
):
    # Download dataset
    download_dataset_task = download_dataset_op(input_bucket=input_bucket)

    # Train model
    train_model_task = train_model_op(download_dataset_task.output)

    # Evaluate model
    evaluate_model_task = evaluate_model_op(download_dataset_task.output, train_model_task.output)

    # Export model
    export_model_task = export_model_op(train_model_task.output, evaluate_model_task.output, export_bucket=export_bucket, model_name=model_name, model_version=model_version)

    # Deploy model using KFServing
    kfserving_task = kfserving_op(export_model_task.output)

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(pipeline_func=end_to_end_mnist_pipeline)

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment(name='End-to-End MNIST Experiment')
run = client.run(experiment_id=experiment.id, pipeline_package_path='pipeline_dev.json')
```

This code snippet defines a Kubeflow Pipeline named `End-to-End MNIST Pipeline` that performs end-to-end machine learning tasks, including data download, model training, evaluation, export, and deployment using KFServing. The pipeline consists of five components, each with its own input and output, and utilizes a base Docker image. The pipeline also includes a KFServing deployment step that occurs after the model export is complete.