```python
import kfp
from kfp import dsl

# Define the echo component
@dsl.component(
    base_image="ubuntu",
    outputs=["output"],
)
def echo():
    return "hello, world"

# Define the echo_pipeline function
@dsl.pipeline(
    name="echo-pipeline",
    description="A simple echo pipeline.",
    parameters=[
        dsl.Parameter("param", type=dsl.INT, default=1),
        dsl.Parameter("weird_param__", type=dsl.STRING, default="default_string"),
    ],
)
def echo_pipeline(param: int = 1, weird_param__: str = "default_string"):
    # Execute the echo component
    echo_task = echo()

# Compile the pipeline
compiler = kfp.v2.compiler.Compiler()
pipeline_spec = compiler.compile(echo_pipeline)

# Submit the pipeline
client = kfp.v2.client.KubeClient.from_service_account_file("path/to/service-account.json")
run_id = client.create_run_from_pipeline_spec(pipeline_spec=pipeline_spec)
print(f"Run ID: {run_id}")
```

In this solution, we define an `echo` component that simply returns the string "hello, world". We then define the `echo_pipeline` function, which calls the `echo` component. The pipeline is compiled and submitted using the Kubeflow Pipelines SDK. The `compile` method converts the pipeline into a specification that can be executed on a Kubernetes cluster. The `create_run_from_pipeline_spec` method submits the pipeline to the Kubernetes cluster, and the run ID is printed out.