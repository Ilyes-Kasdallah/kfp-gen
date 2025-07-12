```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
raw_data_transfer_op = load_component_from_file('raw_data_transfer.yaml')
preprocess_op = load_component_from_file('preprocess.yaml')
hypertrain_op = load_component_from_file('hypertrain.yaml')
train_optimized_hyperparams_op = load_component_from_file('train_optimized_hyperparams.yaml')

# Define the pipeline
@dsl.pipeline(name='crypto')
def crypto_pipeline(project: str, source_bucket: str, target_bucket: str):
    # Step 1: Transfer raw data
    transfer_task = raw_data_transfer_op(
        project=project,
        source_bucket=source_bucket,
        target_bucket=target_bucket
    )

    # Step 2: Preprocess data
    preprocess_task = preprocess_op(
        project=transfer_task.outputs['project'],
        source_bucket=transfer_task.outputs['source_bucket'],
        target_bucket=transfer_task.outputs['target_bucket']
    )

    # Step 3: Hyperparameter tuning
    hypertrain_task = hypertrain_op(
        bucket=preprocess_task.outputs['bucket']
    )

    # Step 4: Train optimized hyperparameters
    train_optimized_hyperparams_task = train_optimized_hyperparams_op(
        hyperparams=hypertrain_task.outputs['hyperparams']
    )
```

This code defines a Kubeflow Pipeline named `crypto` with four components: `raw_data_transfer`, `preprocess`, `hypertrain`, and `train_optimized_hyperparams`. The pipeline uses the `@dsl.pipeline` decorator with the name specified in the user prompt. Each component depends on the output of the preceding component, and the pipeline uses several Google Cloud services such as Google Cloud Storage (GCS), Cloud Dataflow, and Cloud ML Engine. The pipeline takes `project`, `source_bucket`, and `target_bucket` as parameters.