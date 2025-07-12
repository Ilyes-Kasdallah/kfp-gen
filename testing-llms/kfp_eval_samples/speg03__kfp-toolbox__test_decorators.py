```python
from kfp import dsl

# Define the echo component
@dsl.component(
    base_image="tensorflow/tensorflow:latest",
    resources=dsl.ContainerSpec(
        cpus=2,
        memory="16G",
        accelerator_type="NVIDIA_TESLA_T4"
    ),
    cache=True
)
def echo():
    return "hello, world"

# Define the pipeline
@dsl.pipeline(name="echo-pipeline")
def test_decorators():
    # Call the echo component
    echo_op = echo()

# Compile the pipeline
pipeline_spec = test_decorators.to_pipeline_spec()
print(pipeline_spec)
```

This code defines a Kubeflow Pipeline named `echo-pipeline` with a single component `echo`. The `echo` component uses TensorFlow as its base image, specifies resource requests for 2 CPUs, 16GB of memory, and a NVIDIA TESLA T4 GPU, and enables caching. The pipeline is then compiled into a YAML file, which can be executed using Kubeflow Pipelines.