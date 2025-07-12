```python
import kfp
from kfp import dsl
from urllib.parse import urlparse
import os
import re

# Define the download_artifact component
@dsl.component(
    base_image="appropriate/curl",
    output_artifacts=[
        dsl.OutputArtifact("downloaded_file", "File")
    ],
    parameters=[
        dsl.Parameter("url", type=dsl.String),
        dsl.Parameter("download_to", type=dsl.String),
        dsl.Parameter("md5sum", type=dsl.String)
    ]
)
def download_artifact(url: str, download_to: str, md5sum: str):
    # Download the file
    curl_command = f"curl -o {download_to} {url}"
    os.system(curl_command)

    # Check the MD5 checksum
    md5_check_command = f"md5sum {download_to} | awk '{{print $1}}'"
    actual_md5 = os.popen(md5_check_command).read().strip()
    if actual_md5 != md5sum:
        raise ValueError(f"MD5 checksum mismatch: expected {md5sum}, got {actual_md5}")

# Define the training component
@dsl.component(
    base_image=TRAINING_IMAGE,
    output_artifacts=[
        dsl.OutputArtifact("model_output", "File"),
        dsl.OutputArtifact("metrics_output", "File")
    ],
    parameters=[
        dsl.InputArtifact("downloaded_file", "File"),
        dsl.Parameter("script", type=dsl.String)
    ]
)
def training_op(downloaded_file: dsl.InputArtifact, script: str):
    # Construct the command to run the training script
    command = f"/usr/local/bin/python {script} {downloaded_file.path}"

    # Execute the command
    os.system(command)

# Define the main pipeline
@dsl.pipeline(name="my-pipeline")
def my_pipeline():
    # Download the data artifact
    download_task = download_artifact(
        url="https://example.com/data.zip",
        download_to="/tmp/data.zip",
        md5sum="expected_md5_checksum"
    )

    # Train the model
    training_task = training_op(
        downloaded_file=download_task.outputs["downloaded_file"],
        script="train.py"
    )
```

In this solution, we define two components: `download_artifact` and `training_op`. The `download_artifact` component downloads a file from a given URL and checks its MD5 checksum to ensure the integrity of the download. The `training_op` component executes a specified training script using the downloaded data file. The main pipeline orchestrates these components sequentially, ensuring that the training process only starts after the data download is successful.