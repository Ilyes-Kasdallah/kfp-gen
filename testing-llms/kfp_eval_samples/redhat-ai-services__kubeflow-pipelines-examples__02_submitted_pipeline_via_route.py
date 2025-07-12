```python
import kfp
from kfp import dsl

# Define the add component
@dsl.component(
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
    outputs=["output"],
)
def add(a: float, b: float = 4.0):
    return a + b

# Define the main pipeline
@dsl.pipeline(name="add_pipeline")
def add_pipeline(a: float = 1.0, b: float = 7.0):
    # First addition
    result1 = add(a=a, b=b)

    # Second addition
    result2 = add(a=result1, b=b)

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(add_pipeline, package_path='02_submitted_pipeline_via_route.yaml')

# Submit the pipeline
client = kfp.Client()
run = client.create_run_from_package(pipeline_spec=pipeline_spec, arguments={'a': 3.0, 'b': 5.0})
print(f"Run ID: {run.id}")
```

This code snippet defines a Kubeflow Pipeline named `add_pipeline` that performs two additions. The first component, `add`, takes two float inputs, `a` and `b`, and returns their sum as a float. The second component, also named `add`, takes two float inputs, `a` and `b`, and returns their sum as a float. The control flow is sequential: the second `add` component executes after the first. No parallel processing is involved. The pipeline uses the `kfp` library for Kubeflow Pipelines. No other external tools or libraries (like sklearn or Snowflake) are explicitly used. The pipeline takes two float parameters, `a` and `b`, with default values of 1.0 and 7.0 respectively.