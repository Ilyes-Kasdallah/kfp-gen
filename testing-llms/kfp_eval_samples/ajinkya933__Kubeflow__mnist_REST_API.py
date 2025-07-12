```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load the mnist_training_container component
mnist_training_container = load_component_from_file('mnist_training_container.yaml')

# Define the MNIST Pipeline
@dsl.pipeline(name='MNIST Pipeline')
def mnist_pipeline():
    # Create a VolumeOp to mount a 1Gi volume named 'data-volume'
    data_volume = dsl.VolumeOp(
        name='data-volume',
        size='1Gi',
        resources=dsl.Volumespec(storage_class_name='standard'),
        mount_path='/mnt'
    )

    # Mount the data volume to the mnist_training_container component
    mnist_training_container_op = mnist_training_container(
        volume_mounts=[dsl.VolumeMount(data_volume.name, '/mnt')]
    )
```

This code snippet defines a Kubeflow Pipeline named `MNIST Pipeline` that includes a single component `mnist_training_container`. The pipeline creates a 1Gi volume named `data-volume` and mounts it to the `mnist_training_container` component, allowing the data to be persisted across pipeline executions.