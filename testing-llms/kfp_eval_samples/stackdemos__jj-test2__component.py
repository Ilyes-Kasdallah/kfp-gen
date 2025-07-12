```python
import kfp
from kfp import dsl

# Define the download-artifact component
@dsl.component(
    base_image="ubuntu",
    packages_to_install=["curl"],
    output_artifacts=[
        dsl.OutputArtifact("downloaded_file", "File")
    ]
)
def download_artifact(url: str, download_to: str, md5sum: str) -> None:
    import os
    import hashlib
    import subprocess

    # Check if the file already exists and matches the checksum
    if os.path.exists(download_to):
        with open(download_to, 'rb') as f:
            existing_md5 = hashlib.md5(f.read()).hexdigest()
            if existing_md5 == md5sum:
                print(f"File {download_to} already exists and matches the checksum.")
                return

    # Download the file
    subprocess.run(["curl", "-o", download_to, url], check=True)

    # Calculate the MD5 checksum of the downloaded file
    with open(download_to, 'rb') as f:
        calculated_md5 = hashlib.md5(f.read()).hexdigest()

    # Verify the checksum
    if calculated_md5 != md5sum:
        raise ValueError(f"Checksum mismatch for file {download_to}. Expected {md5sum}, got {calculated_md5}")

# Define the training component dynamically based on the script name
def get_training_component(script_name: str) -> dsl.ContainerOp:
    script_path = f"/opt/ml/scripts/{script_name.lower().replace(' ', '-')}.py"
    image = os.getenv("TRAINING_IMAGE") if "TRAINING_IMAGE" in os.environ else "python:3.8-slim"
    arguments = ["--script", script_path]
    return dsl.ContainerOp(
        name=script_name,
        image=image,
        arguments=arguments,
        outputs={
            "output_file": dsl.OutputArtifact("output_file", "File")
        }
    )

# Define the main pipeline
@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Download the data artifact
    download_task = download_artifact(
        url="https://example.com/data.zip",
        download_to="/tmp/data.zip",
        md5sum="expected_md5_checksum"
    )

    # Get the training component dynamically based on the script name
    script_name = "train_model.py"
    training_task = get_training_component(script_name)

    # Link the download task to the training task
    training_task.after(download_task)
```

This code snippet defines a Kubeflow Pipeline named `my_pipeline` that includes two components: `download-artifact` and a dynamically named training component. The `download-artifact` component downloads a data artifact from a specified URL and verifies its integrity using an MD5 checksum. The training component is dynamically created based on the script name and executed within a container. The pipeline ensures that the training component runs after the download component completes.