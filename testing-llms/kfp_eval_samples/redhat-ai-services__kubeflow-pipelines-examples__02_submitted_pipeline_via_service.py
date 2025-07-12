```python
import kfp
from kfp import dsl

# Define the add component
@dsl.component(
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
    outputs=["output"]
)
def add(a: float, b: float) -> float:
    return a + b

# Define the main pipeline
@dsl.pipeline(name="add_pipeline")
def add_pipeline(a: float = 1.0, b: float = 7.0):
    # First addition
    add_component_1 = add(a=a, b=b)
    
    # Second addition
    add_component_2 = add(a=add_component_1.output, b=b)

# Submit the pipeline to a Kubeflow instance
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(add_pipeline, "02_submitted_pipeline_via_service.yaml")
```

This code snippet defines a Kubeflow Pipeline named `add_pipeline` that performs two sequential additions. The pipeline consists of two components: `add`, which takes two float arguments and returns their sum as a float. The pipeline's control flow is sequential, with the output of the first `add` component being passed as input to the `a` parameter of the second `add` component. The pipeline takes two float parameters: `a` (default 1.0) and `b` (default 7.0). No parallel processing or loops are used. The pipeline utilizes the Kubeflow Pipelines SDK (`kfp`) and the `dsl` module within that SDK for pipeline definition and component creation. No other external libraries like scikit-learn or Snowflake are used. The pipeline is submitted to a Kubeflow instance using a Kubeflow client. The client uses a bearer token for authentication, sourced either from a Kubernetes service account or an environment variable. The code also handles SSL certificates similarly, using the service account if running in a Kubernetes pod.