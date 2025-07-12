```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from files
preprocess_op = load_component_from_file('components/preprocess_image.yaml')
train_op = load_component_from_file('components/train_image.yaml')
inference_server_launcher_op = load_component_from_file('components/inference_server_launcher_image.yaml')
webapp_launcher_op = load_component_from_file('components/webapp_launcher_image.yaml')

@dsl.pipeline(name='resnet_cifar10_pipeline')
def resnet_cifar10_pipeline(
    raw_data_dir='/mnt/workspace/raw_data',
    processed_data_dir='/mnt/workspace/processed_data',
    model_dir='/mnt/workspace/saved_model',
    model_name='resnet_graphdef',
    model_version=1,
    epochs=50,
    trtserver_name='trtis',
    webapp_prefix='webapp',
    webapp_port=80
):
    # Preprocess data
    preprocess_task = preprocess_op(raw_data_dir=raw_data_dir, processed_data_dir=processed_data_dir)

    # Train model
    train_task = train_op(processed_data_dir=processed_data_dir, model_name=model_name, model_version=model_version, epochs=epochs, model_dir=model_dir)

    # Launch inference server
    inference_server_task = inference_server_launcher_op(model_dir=model_dir, trtserver_name=trtserver_name)

    # Launch web app
    webapp_task = webapp_launcher_op(trtserver_name=trtserver_name, model_name=model_name, model_version=model_version, webapp_prefix=webapp_prefix, webapp_port=webapp_port)
```

This code defines a Kubeflow Pipeline named `resnet_cifar10_pipeline` that performs end-to-end training and serving of a ResNet model on the CIFAR-10 dataset. The pipeline consists of four components: `PreprocessOp`, `TrainOp`, `InferenceServerLauncherOp`, and `WebappLauncherOp`. The control flow is sequential, with each component running only after its dependencies have been completed. The pipeline uses Kubernetes containers and the Kubeflow Pipelines DSL (`kfp.dsl`).