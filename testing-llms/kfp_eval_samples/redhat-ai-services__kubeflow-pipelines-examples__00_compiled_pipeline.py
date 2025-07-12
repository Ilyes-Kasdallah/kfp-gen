```python
import kfp
from kfp import dsl

# Define the add component
@dsl.component(
    base_image='image-registry.openshift-image-registry.svc:5000/openshift/python:latest',
    outputs=['output']
)
def add(a: float, b: float):
    return a + b

# Define the main pipeline
@dsl.pipeline(name='add_pipeline')
def add_pipeline(a: float = 1.0, b: float = 7.0):
    # First add component execution
    result1 = add(a=a, b=4.0)

    # Second add component execution
    result2 = add(a=result1.output, b=b)

# Compile the pipeline
compiler.Compiler().compile(add_pipeline, '00_compiled_pipeline.py')

# Run the compiled pipeline
client = kfp.Client()
run = client.create_run_from_pipeline_package('00_compiled_pipeline.py', arguments={'a': 1.0, 'b': 7.0})
print(run.id)
```

This code snippet defines a Kubeflow Pipeline named `add_pipeline` that performs two additions. The pipeline consists of two components, each taking two float inputs and returning their sum as a float. The first component is called twice within the pipeline, with inputs `a` (a pipeline parameter with default value 1.0) and `b` (hardcoded to 4.0). The output of this component is then fed as input `a` to a second instance of the `add` component. The second `add` component receives the output of the first `add` component as its `a` input and a pipeline parameter `b` (with default value 7.0) as its `b` input. The output of the second `add` component is the final output of the pipeline, although it's not explicitly returned as a pipeline output. No parallel processing or loops are used. The pipeline uses the `kfp` (Kubeflow Pipelines) library for its definition and compilation. No other external libraries like sklearn or Snowflake are used.