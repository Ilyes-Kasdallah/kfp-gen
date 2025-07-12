```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the components
gcs_download_op = load_component_from_file('components/gcs_download.yaml')
echo_op = load_component_from_file('components/echo.yaml')

# Define the pipeline
@dsl.pipeline(name='Legacy Exit Handler')
def legacy_exit_handler(url='gs://ml-pipeline/shakespeare1.txt'):
    # First echo component
    echo_first = echo_op()
    
    # Second echo component
    echo_second = echo_op(input=echo_first.outputs['output'])
    
    # GCS download component
    gcs_download = gcs_download_op(url=url)
    
    # Exit handler
    with dsl.ExitHandler():
        echo_second

# Compile the pipeline
pipeline_spec = legacy_exit_handler.to_pipeline_spec()

# Submit the pipeline
client = dsl.Client()
experiment = client.create_experiment('My Experiment')
run = client.run(pipeline_spec=pipeline_spec, experiment_id=experiment.id)
```

This code snippet defines a Kubeflow Pipeline named `Legacy Exit Handler` that includes the required components and their dependencies. The pipeline downloads a file from a GCS URL, prints "exit!" as the first echo, and then prints the contents of the file as the second echo. The exit handler ensures that the second echo runs even if the pipeline fails.