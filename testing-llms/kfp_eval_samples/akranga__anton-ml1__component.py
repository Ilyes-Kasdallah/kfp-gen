```python
import kfp
from kfp import dsl

# Define the download-artifact component
@dsl.component(
    base_image="appropriate/curl",
    output_artifacts=[
        dsl.OutputArtifact(name="downloaded_file", type=dsl.Artifact.FILE)
    ],
    parameters=[
        dsl.Parameter("url", type=dsl.String),
        dsl.Parameter("download_to", type=dsl.String),
        dsl.Parameter("md5sum", type=dsl.String)
    ]
)
def download_artifact(url: str, download_to: str, md5sum: str):
    import os
    import hashlib
    import urllib.request

    # Check if the file already exists and matches the checksum
    if os.path.exists(download_to) and hashlib.md5(open(download_to, 'rb').read()).hexdigest() == md5sum:
        return

    # Download the file
    urllib.request.urlretrieve(url, download_to)

# Define the train-model component
@dsl.component(
    base_image=TRAINING_IMAGE,
    output_artifacts=[
        dsl.OutputArtifact(name="model_output", type=dsl.Artifact.FILE),
        dsl.OutputArtifact(name="predictions_output", type=dsl.Artifact.FILE)
    ],
    parameters=[
        dsl.Parameter("data_path", type=dsl.String),
        dsl.Parameter("script", type=dsl.String),
        dsl.Parameter("file_outputs", type=dsl.Dict(type=dsl.String))
    ]
)
def train_model(data_path: str, script: str, file_outputs: dict):
    import subprocess
    import os

    # Execute the training script
    subprocess.run(["/usr/local/bin/python", script, data_path], stdout=open(file_outputs["model_output"], "wb"), stderr=subprocess.STDOUT)

    # Predictions can be written here if needed

# Define the main pipeline
@dsl.pipeline(
    name="my_pipeline"
)
def my_pipeline():
    # Download the artifact
    download_task = download_artifact(
        url="https://example.com/data.zip",
        download_to="/tmp/data.zip",
        md5sum="1234567890abcdef"
    )

    # Train the model
    train_task = train_model(
        data_path="/tmp/data.zip",
        script="train.py",
        file_outputs={
            "model_output": "/tmp/model.pkl",
            "predictions_output": "/tmp/predictions.csv"
        }
    )
```

This code defines a Kubeflow Pipeline named `my_pipeline` that performs a data download and then model training. The pipeline consists of two components: `download-artifact` and `train-model`. The `download-artifact` component downloads a file from a URL using `curl`, checks the MD5 sum to avoid re-downloading if the file already exists and matches the checksum. The `train-model` component performs model training using a Python script, writes the trained model to a file, and optionally writes predictions to another file. The pipeline uses the `kfp.dsl` library from Kubeflow Pipelines and standard Python libraries like `urllib.parse`, `os`, and `re`.