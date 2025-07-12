```python
import kfp
from kfp import dsl

# Define the create_artifact component
@dsl.component(
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
    outputs=["my_artifact"]
)
def create_artifact():
    import pickle
    my_string = "1, 2, 3, 4"
    my_artifact = pickle.dumps(my_string)
    return my_artifact

# Define the consume_artifact component
@dsl.component(
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
    inputs=["my_artifact"]
)
def consume_artifact(my_artifact):
    import pickle
    deserialized_data = pickle.loads(my_artifact)
    print(deserialized_data)

# Define the main pipeline
@dsl.pipeline(name="Artifact Pipeline")
def artifact_pipeline():
    # Create the artifact
    create_task = create_artifact()
    
    # Consume the artifact
    consume_task = consume_artifact(create_task.outputs["my_artifact"])

# Compile the pipeline
compiler.Compiler().compile(artifact_pipeline, "04_artifact_pipeline.yaml")

# Submit the pipeline run
client = kfp.Client()
run = client.create_run_from_pipeline_package("04_artifact_pipeline.yaml", arguments={})
print(f"Run ID: {run.id}")
```

This code snippet defines a Kubeflow Pipeline named `Artifact Pipeline` that performs data serialization and deserialization using Python's `pickle` library. The pipeline consists of two components: `create_artifact` and `consume_artifact`. The `create_artifact` component serializes the string "1, 2, 3, 4" using `pickle` and saves it as an artifact named `my_artifact`. The `consume_artifact` component takes the `my_artifact` artifact as input, deserializes it using `pickle`, and prints its contents to standard output. The pipeline's control flow is sequential, with `consume_artifact` executing after `create_artifact`, with the output artifact `my_artifact` from `create_artifact` passed as input to `consume_artifact`.