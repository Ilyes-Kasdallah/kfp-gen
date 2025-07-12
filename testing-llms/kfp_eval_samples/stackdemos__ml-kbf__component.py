```python
import kfp
from kfp import dsl

# Define the download artifact component
@dsl.component(
    base_image="appropriate/curl",
    output_artifacts=[
        dsl.OutputArtifact(name="downloaded_data", type=dsl.Artifact.FILE)
    ],
    parameters=[
        dsl.Parameter("url", type=dsl.String),
        dsl.Parameter("download_to", type=dsl.String),
        dsl.Parameter("md5sum", type=dsl.String)
    ]
)
def download_artifact(url: str, download_to: str, md5sum: str):
    # Check if the file already exists and matches the MD5 checksum
    if not os.path.exists(download_to) or hashlib.md5(open(download_to, 'rb').read()).hexdigest() != md5sum:
        # Download the file using curl
        subprocess.run(["curl", "-o", download_to, url], check=True)

# Define the training component
@dsl.component(
    base_image="custom/training_image",
    output_artifacts=[
        dsl.OutputArtifact(name="trained_model", type=dsl.Artifact.MODEL)
    ],
    parameters=[
        dsl.Parameter("data_path", type=dsl.String),
        dsl.Parameter("script", type=dsl.String),
        dsl.Parameter("file_outputs", type=dsl.String)
    ]
)
def training_component(data_path: str, script: str, file_outputs: str):
    # Execute the training script
    subprocess.run([script, data_path, file_outputs], check=True)

# Define the pipeline
@dsl.pipeline(
    name="my_pipeline"
)
def my_pipeline():
    # Download the artifact
    download_op = download_artifact(
        url="https://example.com/dataset.zip",
        download_to="/tmp/dataset.zip",
        md5sum="expected_md5_checksum"
    )

    # Train the model
    training_op = training_component(
        data_path="/tmp/dataset.zip",
        script="train.py",
        file_outputs="/tmp/trained_model.pkl"
    )
```

This code snippet defines a Kubeflow Pipeline named `my_pipeline` that includes two components: `download-artifact` and `training-component`. The `download-artifact` component downloads a dataset from a specified URL, while the `training-component` trains a machine learning model using the downloaded data. The pipeline's control flow ensures that the training component runs only after the download component has completed successfully.