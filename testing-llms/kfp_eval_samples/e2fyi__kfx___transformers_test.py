```python
from kfp import dsl
from kfx.dsl._transformers import ContainerOpTransform

# Define the pipeline
@dsl.pipeline(name="KubeflowContainerOpTransformPipeline")
def _transformers_test():
    # Create a sample ContainerOp
    sample_container_op = dsl.ContainerOp(
        name="SampleContainerOp",
        image="example-image",
        command=["echo", "Hello, World!"],
        resources=dsl.Resources(requests={"cpu": "100m", "memory": "512Mi"}),
        annotations={"app.kubernetes.io/name": "sample-app"},
        labels={"app.kubernetes.io/version": "v1"}
    )

    # Apply transformations to the ContainerOp
    transformed_container_op = ContainerOpTransform(sample_container_op)

    # Output the transformed ContainerOp
    transformed_container_op.output("transformed_container_op")

# Execute the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(_transformers_test, package_path="transformers_pipeline.yaml")
```

This code snippet defines a Kubeflow Pipeline named `KubeflowContainerOpTransformPipeline` that includes a single component `ContainerOpTransformationComponent`. The component modifies a given `ContainerOp` by setting various attributes such as `imagePullPolicy`, resource requests and limits, annotations, and labels. The pipeline executes the transformation and outputs the modified `ContainerOp`.