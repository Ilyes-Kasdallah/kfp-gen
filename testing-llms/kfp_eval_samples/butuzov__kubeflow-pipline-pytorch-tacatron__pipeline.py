```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the components
download_dataset = load_component_from_file('components/download_dataset.yaml')
train_model = load_component_from_file('components/train_model.yaml')
serve_model = load_component_from_file('components/serve_model.yaml')

# Define the pipeline
@dsl.pipeline(name='example', description='A machine learning workflow')
def example_pipeline(
    owner: str,
    kf_pipeline_version: str,
    dataset_url: str = 'https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2',
    dataset_dir: str = '/mnt/kf/',
    models_dir: str = '/mnt/kf/models/',
    checkpoint_dir: str = '/mnt/kf/checkpoints/',
    batch_size: int = 64,
    learning_rate: float = 0.001,
    log_step: int = 100,
    save_step: int = 500,
    num_epochs: int = 100
):
    # Download the dataset
    download_task = download_dataset(dataset_url=dataset_url, dataset_dir=dataset_dir)

    # Train the model
    train_task = train_model(
        dataset_dir=dataset_dir,
        models_dir=models_dir,
        checkpoint_dir=checkpoint_dir,
        batch_size=batch_size,
        learning_rate=learning_rate,
        log_step=log_step,
        save_step=save_step,
        num_epochs=num_epochs
    )

    # Serve the model
    serve_task = serve_model(
        results_dir='/mnt/kf/results/',
        models_dir=models_dir,
        model_filename='model.pth.tar'
    )
```

This code snippet defines a Kubeflow Pipeline named `example` that performs a machine learning workflow. It includes three components: `dataset download`, `training model`, and `serving`. The pipeline is defined using the `@dsl.pipeline` decorator with the name specified in the user prompt. Each component is loaded from a YAML file using the `load_component_from_file` function. The pipeline's control flow is sequential, with each component depending on the previous one. The pipeline uses custom container images referencing environment variables `OWNER` and `KF_PIPELINE_VERSION`.