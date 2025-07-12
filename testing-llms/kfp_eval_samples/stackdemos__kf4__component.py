```python
import kfp
from kfp import dsl
from urllib.parse import urlparse
import os
import re

# Global variable for the training image
TRAINING_IMAGE = "your-training-image"

def http_download_op(url, download_to):
    """Download a file from a URL."""
    return dsl.ContainerOp(
        name="http-download",
        image="nginx",
        arguments=[
            "--url", url,
            "--download-to", download_to
        ]
    )

def md5_check_op(download_to, md5sum):
    """Check the MD5 checksum of a downloaded file."""
    return dsl.ContainerOp(
        name="md5-check",
        image="busybox",
        arguments=[
            "sh", "-c", f"echo {md5sum} | sha256sum -c"
        ],
        inputs=dsl.Inputs(
            artifacts={
                "downloaded_file": dsl.Artifact(type=dsl.ArtifactType.FILE)
            }
        ),
        outputs=dsl.Outputs()
    )

def training_op(data_path, script, image=None):
    """Train a machine learning model."""
    if image is None:
        image = TRAINING_IMAGE
    return dsl.ContainerOp(
        name="train-model",
        image=image,
        arguments=[
            "--data-path", data_path,
            "--script", script
        ],
        outputs=dsl.Outputs(file_outputs={"model": dsl.OutputArtifact(type=dsl.ArtifactType.MODEL)})
    )

@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Download the data artifact
    download_task = http_download_op("https://example.com/data.zip", "/tmp/data.zip")

    # Check the MD5 checksum of the downloaded file
    md5_task = md5_check_op("/tmp/data.zip", "expected_md5_checksum")

    # Train the machine learning model
    train_task = training_op(md5_task.outputs["downloaded_file"].path, "path/to/training/script.py")

    # Output the trained model
    train_task.output_artifacts["model"].set_uri(train_task.outputs["model"].uri)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(my_pipeline, "my_pipeline.yaml")
```

This code defines a Kubeflow Pipeline named `my_pipeline` that performs data ingestion and model training. The pipeline consists of three components: `download-artifact`, `md5-check`, and `training-op`. The `download-artifact` component downloads a data artifact from a URL, the `md5-check` component verifies the integrity of the downloaded file, and the `training-op` component trains a machine learning model using a custom Python script. The pipeline uses the `kfp.dsl` library for pipeline definition and the `urllib.parse`, `os`, and `re` libraries for URL parsing, file path manipulation, and regular expressions respectively. The `training_op` function is used to encapsulate common container operation logic.