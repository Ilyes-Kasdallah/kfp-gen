```python
import kfp
from kfp import dsl

# Load environment variables from .env file
kfp.components.load_env()

@dsl.pipeline(name='container-pipeline')
def add(a=1.0, b=7.0):
    # Define the add component
    @dsl.component(
        base_image='quay.io/rhiap/kubeflow-example:latest',
        command=['sh', '-c', 'python components/add.py']
    )
    def add_op(a, b):
        return a + b

    # Execute the add component
    add_task = add_op(a=a, b=b)

# Compile the pipeline
compiler.Compiler().compile(add, '07_container_components_pipeline.yaml')

# Submit the pipeline to Kubeflow
client = kfp.Client(endpoint='https://your-kubeflow-endpoint.com', bearer_token='your-bearer-token')
run = client.create_run_from_pipeline_file('07_container_components_pipeline.yaml')
```

In this solution, we first load the environment variables from a `.env` file using `kfp.components.load_env()`. We then define a pipeline named `container-pipeline` using the `@dsl.pipeline` decorator. Inside the pipeline, we define a single component named "add" using the `@dsl.component` decorator. This component uses the Docker image `quay.io/rhiap/kubeflow-example:latest` and executes the Python script `components/add.py` using `sh -c`. The script's internal logic is assumed to perform an addition operation based on the pipeline's name and description. The pipeline's control flow is straightforward; it's a single component with no branching or looping. No parallelFor or specific dependency structures are employed. The pipeline utilizes the `kfp.dsl.ContainerOp` function to define the component. Finally, we compile the pipeline using the `Compiler()` class and submit it to a Kubeflow instance using the Kubeflow Python client.