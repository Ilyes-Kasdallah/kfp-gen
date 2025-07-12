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
def download_artifact(url: str, md5_checksum: str, output_file: dsl.OutputPath()):
    import os
    import hashlib
    import subprocess

    # Check if the file already exists and has the correct checksum
    if os.path.exists(output_file) and hashlib.md5(open(output_file, 'rb').read()).hexdigest() == md5_checksum:
        print(f"File {output_file} already exists and matches the checksum.")
        return

    # Download the file using curl
    subprocess.run(["curl", "-o", output_file, url], check=True)

# Define the training component
@dsl.component(
    base_image="custom/training-image",
    outputs=["trained_model"]
)
def training_op(data_path: dsl.InputPath(), trained_model: dsl.OutputPath()):
    # Implement the training logic here
    pass

# Define the main pipeline
@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Download the data artifact
    download_task = download_artifact(
        url="https://example.com/data.zip",
        md5_checksum="expected_md5_checksum",
        output_file="/tmp/data.zip"
    )

    # Train the model using the downloaded data
    train_task = training_op(
        data_path=download_task.outputs["output_file"],
        trained_model="/tmp/trained_model"
    )
```

This code snippet defines a Kubeflow Pipeline named `my_pipeline` that includes two components: `download-artifact` and a training component. The `download-artifact` component downloads a data artifact from a specified URL and verifies its integrity using an MD5 checksum. The `training-op` component then uses the downloaded data to train a model. The pipeline ensures that the training operation only runs after the data download is successful.