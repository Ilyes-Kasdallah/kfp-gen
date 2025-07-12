```python
import kfp
from kfp import dsl

# Import necessary libraries
from kfp.components import load_component_from_text

# Load the hello component from text
hello_component = load_component_from_text("""
apiVersion: pipelines.kubeflow.org/v1alpha1
kind: Component
metadata:
  name: hello
spec:
  description: A simple component that prints a message.
  inputs:
    - name: message
      type: string
      default: "hello world"
  outputs:
    - name: result
      type: string
""")

# Define the pipeline
@dsl.pipeline(name="hello-world-pipeline")
def hello_world_pipeline(job_id="xxxx", message="hello world"):
    # Execute the hello component
    hello_task = hello_component(message=message)
    
    # Set retry mechanism
    hello_task.set_retry(num_retries=2)

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(hello_world_pipeline, package_path='hello-world-pipeline.yaml')

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment("Hello World Experiment")
run = client.run(experiment.id, pipeline_name="hello-world-pipeline", pipeline_package_path='hello-world-pipeline.yaml')
```

In this solution, we define a Kubeflow Pipeline named `hello-world-pipeline` using the `@dsl.pipeline` decorator. We also define a component called `hello` using the `load_component_from_text` function. The pipeline includes a single task that invokes the `hello` component with specified inputs and sets a retry mechanism. Finally, we compile the pipeline and submit it to the Kubeflow Pipelines server.