```python
from kfp import dsl
from kfp.components import create_custom_training_job_from_component

# Download Dataset Component
@dsl.component(
    base_image='davidnet/cbis_ddsm_dataloader:1.0.2',
    packages_to_install=[
        'tensorflow-datasets',
        'opencv-python-headless',
        'tensorflow'
    ],
    output_artifact_path='downloaded_dataset.tar.gz'
)
def download_dataset():
    pass

# Create TF Records Component
@dsl.component(
    base_image='python:3.12',
    packages_to_install=[
        'tensorflow-datasets',
        'opencv-python-headless',
        'tensorflow'
    ],
    output_artifact_path='tf_records.tar.gz'
)
def create_tf_records(dataset_artifact):
    # Implement TF Record creation logic here
    pass

# Train Model Component
@dsl.component(
    base_image='davidnet/flax-cnn-model:1.0.0',
    packages_to_install=[
        'tensorflow'
    ],
    output_artifact_path='trained_model.tar.gz'
)
def train_model(tf_records_artifact,
                 train_steps=1000,
                 eval_every=500,
                 batch_size=32,
                 learning_rate=0.001,
                 momentum=0.9):
    # Implement model training logic here
    pass

# Pipeline Definition
@dsl.pipeline(name='CBIS-DDSM-Training-Pipeline')
def cbis_ddsm_training_pipeline():
    # Download Dataset
    download_task = download_dataset()

    # Create TF Records
    tf_records_task = create_tf_records(download_task.output)

    # Train Model
    train_model_task = train_model(tf_records_task.output,
                                  train_steps=1000,
                                  eval_every=500,
                                  batch_size=32,
                                  learning_rate=0.001,
                                  momentum=0.9)

# Execute the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(cbis_ddsm_training_pipeline, 'cbis_ddsm_training_pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `CBIS-DDSM-Training-Pipeline` that performs image classification on the CBIS-DDSM dataset. It includes three components: `Download Dataset`, `Create TF Records`, and `Train Model`. Each component is defined using the `@dsl.component` decorator, specifying the base image, required packages, and output artifact path. The pipeline is executed by compiling it into a YAML file using `kfp.compiler.Compiler()`.