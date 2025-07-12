```python
import kfp
from kfp import dsl

# Import necessary modules
from google.cloud import storage
import subprocess

# Define the GCS - Download component
@gcp.container_op(name="GCS - Download", image="google/cloud-sdk:279.0.0")
def gcs_download(url="gs://ml-pipeline/shakespeare/shakespeare1.txt"):
    # Create a client for interacting with GCS
    storage_client = storage.Client()
    
    # Get the bucket and object
    bucket_name = url.split("//")[1].split("/")[0]
    blob_name = url.split("/")[-1]
    
    # Download the file
    blob = storage_client.bucket(bucket_name).blob(blob_name)
    blob.download_to_filename("/tmp/results.txt")

# Define the echo component
@gcp.container_op(name="echo", image="library/bash:4.4.23")
def echo(text):
    # Execute the echo command
    subprocess.run(["echo", text], check=True)

# Define the Exit Handler
@dsl.exit_handler
def exit_handler():
    # Print "exit!"
    print("exit!")

# Define the pipeline
@dsl.pipeline(name="Exit Handler")
def exit_handler_pipeline():
    # Call the GCS - Download component
    gcs_download()
    
    # Call the first echo component
    echo(gcs_download.outputs["content"])
    
    # Call the second echo component (exit handler)
    with exit_handler():
        echo("exit!")

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(exit_handler_pipeline)

# Submit the pipeline run
client = kfp.Client()
run = client.create_run_from_pipeline_func(compiled_pipeline, arguments={})
print(f"Run ID: {run.id}")
```

This code snippet defines a Kubeflow Pipeline named `Exit Handler` that performs a simple data download and echo operation, demonstrating the use of an exit handler. The pipeline consists of three components: `GCS - Download`, `echo` (used twice), and an `Exit Handler`. The pipeline's control flow is as described in the problem statement.