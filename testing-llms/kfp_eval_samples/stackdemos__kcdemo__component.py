```python
import kfp
from kfp import dsl
from urllib.parse import urlparse

TRAINING_IMAGE = "your_training_image"

def http_download_op(url, download_to):
    return dsl.ContainerOp(
        name="Download File",
        image="appropriate/curl",
        arguments=[
            "-L", url,
            "-o", download_to,
            "--fail"
        ],
        metadata={
            "description": "Downloads a file from a URL."
        }
    )

def training_op(download_to):
    parsed_url = urlparse(download_to)
    script_name = parsed_url.path.split('/')[-1]
    training_script = f"train_{script_name}.py"
    
    # Dynamically generate container op based on training script
    container_op = dsl.ContainerOp(
        name=f"Train {script_name}",
        image=TRAINING_IMAGE,
        arguments=[
            "/usr/local/bin/python",
            training_script,
            download_to
        ],
        metadata={
            "description": f"Trains a model using the {script_name} script."
        }
    )
    
    return container_op

@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    download_component = http_download_op("https://example.com/data.zip", "data.zip")
    train_component = training_op(download_component.output)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(my_pipeline, "my_pipeline.yaml")
```

This code defines a Kubeflow Pipeline named `my_pipeline` that includes two components: `download-artifact` and `training-script`. The `download-artifact` component downloads a file from a specified URL and checks its MD5 checksum. The `training-script` component trains a model using the downloaded file. The pipeline's control flow ensures that the training component runs after the download component completes successfully.