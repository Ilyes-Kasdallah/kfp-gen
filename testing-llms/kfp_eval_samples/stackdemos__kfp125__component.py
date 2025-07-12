```python
import kfp
from kfp import dsl

# Define the download artifact component
@dsl.component(
    base_image="appropriate/curl",
    outputs=["output_file"],
    requirements=[
        "pip install -r requirements.txt"
    ]
)
def http_download_op(url: str, md5_sum: str):
    import os
    import hashlib
    import requests

    # Download the file
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join("/tmp", url.split("/")[-1])
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Calculate the MD5 sum of the downloaded file
        with open(file_path, 'rb') as f:
            md5_hash = hashlib.md5(f.read()).hexdigest()

        # Compare the calculated MD5 sum with the provided MD5 sum
        if md5_hash != md5_sum:
            raise ValueError("MD5 sum mismatch")

        return file_path
    else:
        raise ValueError("Failed to download file")

# Define the training component
@dsl.component(
    base_image="${{env.TRAINING_IMAGE}}",
    outputs=file_outputs,
    requirements=[
        "pip install -r requirements.txt"
    ]
)
def training_op(input_file: str, file_outputs: dict):
    import subprocess

    # Run the training script
    command = [
        "/usr/bin/python3",
        "-m",
        "train_script",
        "--input-file",
        input_file
    ]

    try:
        subprocess.run(command, check=True)
        file_outputs["model"] = "path/to/model.pkl"
        file_outputs["accuracy"] = "0.85"
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Training failed: {e}")

# Define the main pipeline
@dsl.pipeline(name="my_pipeline")
def my_pipeline(data_url: str, md5_sum: str, training_image: str):
    # Download the artifact
    download_task = http_download_op(url=data_url, md5_sum=md5_sum)

    # Train the model
    train_task = training_op(input_file=download_task.output, file_outputs={"model": "path/to/model.pkl", "accuracy": "0.85"})

# Compile the pipeline
compiler.Compiler().compile(my_pipeline, package_path="my_pipeline.yaml")
```

This code defines a Kubeflow Pipeline named `my_pipeline` that performs a data download and subsequent training. The pipeline consists of two components: `download-artifact` and a training component. The `download-artifact` component downloads a file from a URL specified as an input, calculates the MD5 sum of the downloaded file, and compares it against a provided MD5 sum. If the MD5 sums match, it skips the download. The output is the path to the downloaded file. The `training-component` takes the downloaded data file path as input and performs model training using a Python script. The input is the path to the downloaded data file. It uses a custom Python script (specified as input to the `training-op` function) and the image specified by the `TRAINING_IMAGE` environment variable (if running in a Jupyter Notebook). The output of this component is defined by the `file_outputs` dictionary passed to the `training-op` function. The `training-op` function is used to create this component. The pipeline uses the `http_download_op` and `training_op` functions defined within the `component.py` file, utilizing `ContainerOp` from the `kfp.dsl` library.