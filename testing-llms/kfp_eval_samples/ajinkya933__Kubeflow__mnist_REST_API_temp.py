```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_text

# Load the train component from text
train_op = load_component_from_text("""
apiVersion: kfp.v2
kind: Component
metadata:
  name: train
spec:
  description: Train a Keras model on the MNIST Fashion dataset.
  inputs:
    - {name: data_path, type: string, default: /mnt}
    - {name: model_file, type: string, default: mnist_model.h5}
  outputs:
    - {name: trained_model, type: artifact}
    - {name: test_data, type: artifact}
  implementation:
    container:
      image: tensorflow/tensorflow:latest-gpu-py3
      command:
        - python
        - -m
        - keras.applications.mnist
        - train
        - --data-path=${{inputs.data_path}}
        - --model-file=${{inputs.model_file}}
""")

# Define the main pipeline
@dsl.pipeline(name="MNIST Pipeline")
def mnist_pipeline():
    # Create a persistent volume for storing data
    data_volume = dsl.VolumeOp(
        name="data-volume",
        size="1Gi"
    )

    # Mount the persistent volume to the container
    mount_volume = dsl.VolumeMount(
        name="data-volume",
        mount_path="/mnt"
    )

    # Run the train component with the mounted volume
    train_task = train_op(
        data_path=dsl.InputValue("data-volume"),
        model_file=dsl.OutputPath("trained_model")
    )

    # Save the test data as an artifact
    test_data_artifact = dsl.Artifact(type=dsl.ArtifactType.DATAFRAME)
    test_data_task = dsl.ContainerOp(
        name="save-test-data",
        image="python:3.8-slim",
        command=["python", "-c", "import pandas as pd; df = pd.DataFrame({'image': [1], 'label': [2]}); df.to_pickle('/mnt/test_data')"],
        volumes=[mount_volume],
        outputs=[test_data_artifact]
    )

    # Link the train task to the save test data task
    train_task.after(test_data_task)

# Compile the pipeline to a YAML file
kfp.compiler.Compiler().compile(mnist_pipeline, "mnist_REST_API_temp.yaml")
```

This code defines a Kubeflow Pipeline named `MNIST Pipeline` that performs a complete MNIST model training workflow. The pipeline uses a single component, which trains a Keras model on the MNIST Fashion dataset. The pipeline leverages a Docker container (`tensorflow/tensorflow:latest-gpu-py3`) for training. The pipeline uses a persistent volume (`data-volume`, size 1Gi) that's mounted into the container, allowing the component to access and write to the persistent storage. The pipeline compiles to a YAML file named `mnist_REST_API_temp.yaml`.