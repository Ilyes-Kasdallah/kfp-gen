```python
import kfp
from kfp import dsl

# Import necessary modules
import urllib.parse
import os
import re

# Define the download_artifact component
@dsl.component(
    base_image="appropriate/curl",
    output_artifacts=[
        dsl.OutputArtifact(name="downloaded_file", type=dsl.Artifact.FILE)
    ],
    parameters=[
        dsl.Parameter("url", type=dsl.String),
        dsl.Parameter("md5sum", type=dsl.String),
        dsl.Parameter("download_to", type=dsl.String)
    ]
)
def download_artifact(url: str, md5sum: str, download_to: str):
    # Construct the command to download the file
    cmd = f"curl -o {download_to} {url}"
    
    # Check the MD5 sum of the downloaded file
    md5_check_cmd = f"echo '{md5sum}' | md5sum -c"
    md5_check_output = os.popen(md5_check_cmd).read().strip()
    
    # If the MD5 sum matches, execute the download command
    if md5_check_output == "OK":
        os.system(cmd)
    else:
        raise ValueError(f"MD5 sum mismatch for {download_to}")

# Define the training_component
@dsl.component(
    base_image=TRAINING_IMAGE,
    output_artifacts=[
        dsl.OutputArtifact(name="model", type=dsl.Artifact.MODEL)
    ],
    parameters=[
        dsl.Parameter("script", type=dsl.String),
        dsl.Parameter("arguments", type=dsl.List(type=dsl.String), optional=True)
    ]
)
def training_op(script: str, arguments: list = None):
    # Execute the training script
    cmd = f"/usr/local/bin/python {script}"
    if arguments:
        cmd += f" {' '.join(arguments)}"
    os.system(cmd)

# Define the main pipeline
@dsl.pipeline(
    name="my-pipeline",
    description="A data download and model training workflow."
)
def my_pipeline():
    # Download the artifact
    download_task = download_artifact(
        url="https://example.com/data.zip",
        md5sum="1234567890abcdef",
        download_to="/tmp/data.zip"
    )
    
    # Train the model using the downloaded artifact
    train_task = training_op(
        script="/path/to/training_script.py",
        arguments=["--data", "/tmp/data.zip"]
    )

# Compile the pipeline
compiler.Compiler().compile(my_pipeline, package_path="my_pipeline.yaml")
```

This code snippet defines a Kubeflow Pipeline named `my-pipeline` that performs a data download and model training workflow. The pipeline consists of two components: `download-artifact` and `training-op`. The `download-artifact` component downloads a file from a specified URL using `curl` and checks its MD5 sum to avoid redundant downloads. The `training-op` component performs model training using a Python script. The pipeline's control flow is sequential, and the output of the download component is implicitly passed as an argument to the training component.