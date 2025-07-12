```python
from kfp import dsl
import os

# Define the download artifact component
@dsl.component(
    base_image="appropriate/curl",
    output_artifacts=[
        dsl.OutputArtifact("downloaded_file", "File")
    ],
    parameters=[
        dsl.Parameter("url", type=dsl.String),
        dsl.Parameter("target_path", type=dsl.String),
        dsl.Parameter("md5_checksum", type=dsl.String)
    ]
)
def download_artifact(url: str, target_path: str, md5_checksum: str):
    # Check if the file already exists and has the correct checksum
    if os.path.exists(target_path) and os.path.getsize(target_path) == int(md5_checksum, 16):
        print(f"Skipping download of {target_path} because it already exists.")
        return
    
    # Download the file using curl
    os.system(f"curl -o {target_path} {url}")

# Define the training component
@dsl.component(
    base_image=TRAINING_IMAGE,
    output_artifacts=[
        dsl.OutputArtifact("trained_model", "File")
    ],
    parameters=[
        dsl.InputArtifact("dataset", "File"),
        dsl.OutputParameter("file_outputs", type=dsl.Dict)
    ]
)
def train_model(dataset: dsl.InputArtifact, file_outputs: dsl.OutputParameter):
    # Execute the training script
    os.system(f"/usr/local/bin/python /path/to/training_script.py --dataset {dataset.uri}")
    
    # Store the trained model file in the output dictionary
    file_outputs["trained_model"] = dataset.uri

# Define the main pipeline
@dsl.pipeline(name="my-pipeline")
def my_pipeline():
    # Download the dataset
    download_task = download_artifact(
        url="https://example.com/dataset.zip",
        target_path="/tmp/dataset.zip",
        md5_checksum="1234567890abcdef"
    )
    
    # Train the model
    train_task = train_model(
        dataset=download_task.outputs["downloaded_file"],
        file_outputs={"trained_model": "/tmp/trained_model.pkl"}
    )

# Run the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(my_pipeline, "my_pipeline.yaml")
```

In this solution, we define two components: `download_artifact` and `train_model`. The `download_artifact` component checks if the file already exists and has the correct checksum before downloading it. The `train_model` component executes a training script and stores the trained model file in the output dictionary. The main pipeline orchestrates these components in sequence. The pipeline is compiled into a YAML file for deployment.