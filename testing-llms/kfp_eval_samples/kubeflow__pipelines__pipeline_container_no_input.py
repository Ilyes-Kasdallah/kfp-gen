```python
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='v2-container-component-no-input')
def pipeline_container_no_input():
    # Define the component
    @dsl.component(
        base_image='python:3.7',
        command=['echo', 'hello world']
    )
    def container_no_input():
        pass

    # Execute the component
    container_no_input()
```

This code snippet defines a Kubeflow Pipeline named `v2-container-component-no-input` with a single component `container_no_input` that uses a Docker container with the image `python:3.7`. The component executes the command `echo hello world`, which writes the string "hello world" to standard output within the container. The pipeline's output is implicitly the output of the `echo` command, written to standard output within the container.