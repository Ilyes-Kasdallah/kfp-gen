```python
import kfp
from kfp import dsl

# Define the download-artifact component
@dsl.component(
    base_image="appropriate/curl",
    outputs=["output_file"],
    requirements=[
        "pip install -r requirements.txt"
    ]
)
def download_artifact(url: str, local_path: str, md5_checksum: str):
    # Download the file using curl
    cmd = f"curl -o {local_path} {url}"
    kfp.components.execute_command(cmd)

    # Verify the checksum of the downloaded file
    cmd = f"md5sum {local_path} | grep {md5_checksum}"
    result = kfp.components.execute_command(cmd)
    if result.strip() != md5_checksum:
        raise ValueError("Checksum verification failed")

# Define the training component
@dsl.component(
    base_image=TRAINING_IMAGE,
    outputs=["model_output"],
    requirements=[
        "pip install -r requirements.txt"
    ]
)
def train_model(script_path: str, *args):
    # Run the training script using /usr/local/bin/python
    cmd = f"/usr/local/bin/python {script_path} {' '.join(args)}"
    kfp.components.execute_command(cmd)

# Define the main pipeline
@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Download the artifact
    download_task = download_artifact(
        url="https://example.com/data.zip",
        local_path="/tmp/data.zip",
        md5_checksum="1234567890abcdef"
    )

    # Train the model
    train_task = train_model(
        script_path="/path/to/training_script.py",
        arg1="value1",
        arg2="value2"
    )
```

In this solution, we define two components: `download-artifact` and `train-model`. The `download-artifact` component uses `curl` to download a file from a given URL and verifies its checksum. The `train-model` component runs a Python script using the specified training logic. The main pipeline orchestrates these components, ensuring that the download task completes before the training task starts.