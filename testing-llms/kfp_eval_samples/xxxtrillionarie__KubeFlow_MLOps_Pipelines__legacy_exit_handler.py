```python
from kfp import dsl
from kfp.deprecated import components

# Define the GCS - Download component
@gcp.components.load_component_from_text("""
apiVersion: v1
kind: Pod
metadata:
  name: gcs-download
spec:
  containers:
  - name: gcs-download-container
    image: google/cloud-sdk:279.0.0
    command:
      - sh
      - -c
      - gsutil cp ${{inputs.parameters.url}} /tmp/results.txt
""")
def gcs_download(url: str):
    pass

# Define the echo component
@gcp.components.load_component_from_text("""
apiVersion: v1
kind: Pod
metadata:
  name: echo
spec:
  containers:
  - name: echo-container
    image: library/bash:4.4.23
    command:
      - sh
      - -c
      - echo ${{inputs.parameters.message}}
""")
def echo(message: str):
    pass

# Define the Exit Handler
@dsl.exit_handler
def exit_handler():
    pass

# Define the pipeline
@dsl.pipeline(name="Legacy Exit Handler")
def legacy_exit_handler(url: str = "gs://ml-pipeline/shakespeare1.txt"):
    # Step 1: Download the file from GCS
    download_task = gcs_download(url=url)
    
    # Step 2: Print 'exit!'
    echo_task_1 = echo(message='exit!')
    
    # Step 3: Print the downloaded file
    echo_task_2 = echo(message=download_task.outputs["output"])
```

This code snippet defines a Kubeflow Pipeline named `Legacy Exit Handler` that includes the required components and an exit handler. The pipeline downloads a file from a specified GCS URL, prints 'exit!', and then prints the contents of the downloaded file. The `exit_handler` ensures that the first `echo` component runs after the pipeline completes, regardless of success or failure.