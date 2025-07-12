```python
import kfp
from kfp import dsl

# Importing the sys module to simulate a failure
import sys

# Defining the fail component
@dsl.component(
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.DIRECTORY)
)
def fail():
    # Simulating a failure by exiting with a return code of 1
    sys.exit(1)

# Defining the main pipeline
@dsl.pipeline(name="fail-pipeline")
def fail_pipeline():
    # Executing the fail component
    fail()

# Creating the pipeline client
client = kfp.Client()

# Submitting the pipeline run
run = client.create_run_from_pipeline_func(fail_pipeline, arguments={})

print("Pipeline run ID:", run.id)
```

This code snippet defines a Kubeflow Pipeline named `fail-pipeline` that includes a single component: the `fail` component. The `fail` component simulates a failure by exiting with a return code of 1. The pipeline's control flow is straightforward, executing the `fail` component without any parallel execution or conditional logic. The component uses the standard Python `sys` library to trigger the failure. The pipeline is then submitted to the Kubeflow Pipelines server using the `create_run_from_pipeline_func` method of the pipeline client.