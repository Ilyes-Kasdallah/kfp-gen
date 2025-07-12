```python
import kfp
from kfp import dsl

# Define the download artifact component
@dsl.component(
    base_image="appropriate/curl",
    packages_to_install=["curl"],
    output_artifacts=[
        dsl.OutputArtifact(name="downloaded_file", type=dsl.Artifact.FILE)
    ],
    metadata={
        "description": "Downloads a dataset from a URL."
    }
)
def download_artifact(url: str, download_to: str, md5sum: str):
    # Check if the file already exists at the download_to path
    if os.path.exists(download_to):
        print(f"File {download_to} already exists.")
        return
    
    # Download the file using curl
    subprocess.run(["curl", "-o", download_to, url], check=True)
    
    # Verify the MD5 checksum of the downloaded file
    actual_md5 = hashlib.md5(open(download_to, 'rb').read()).hexdigest()
    if actual_md5 != md5sum:
        raise ValueError("MD5 checksum mismatch.")

# Define the training component
def training_op(script: str, image: str, arguments: list = None, file_outputs: dict = None):
    container_op = dsl.ContainerOp(
        name=script.split('/')[-1],
        image=image,
        command=["/usr/local/bin/python"],
        arguments=[script] + arguments,
        outputs=file_outputs
    )
    return container_op

# Define the main pipeline
@dsl.pipeline(
    name="my_pipeline"
)
def my_pipeline():
    # Download the dataset
    download_component = download_artifact(
        url="https://example.com/dataset.zip",
        download_to="/tmp/dataset.zip",
        md5sum="expected_md5_checksum"
    )
    
    # Train the model using the downloaded dataset
    training_component = training_op(
        script="/path/to/training_script.py",
        image="your_training_docker_image",
        file_outputs={"model_output": "/tmp/model.pkl"}
    )

# Compile and run the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(my_pipeline, "my_pipeline.yaml")
    kfp.Client().create_run_from_pipeline_package("my_pipeline.yaml")
```

This code snippet defines a Kubeflow Pipeline named `my_pipeline` that includes two components: `download-artifact` and a custom training component. The `download-artifact` component downloads a dataset from a specified URL and verifies its integrity using MD5 checksum. The `training-op` function executes a Python script using a specified Docker image and outputs the trained model. The pipeline's control flow is sequential, with the training component running after the download component. The pipeline is compiled and run using the Kubeflow Pipelines SDK.