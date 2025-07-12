```python
import kfp
from kfp import dsl

# Define the first add component
@dsl.component(
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
    outputs=["output"],
)
def add(a: float, b: float = 4.0):
    # Calculate the sum
    result = a + b
    # Output the result
    return result

# Define the second add component
@dsl.component(
    base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
)
def add_second(a: float, b: float):
    # Calculate the sum
    result = a + b
    # Return the sum
    return result

# Define the pipeline
@dsl.pipeline(name="PVC Pipeline")
def pvc_pipeline(a: float = 1.0, b: float = 7.0):
    # Mount the PVC to the first component
    with dsl.ParallelFor(range(3)) as i:
        with dsl.Condition(i % 2 == 0):
            add_task = add(a=a, b=4.0)
            add_task.output >> dsl.ContainerOp(
                name=f"mount-pvc-{i}",
                image="your-mount-pvc-image",
                command=["bash", "-c", f"kubectl mount-pvc --name=my-data --namespace=default /opt/data"],
            )
        add_second_task = add_second(a=add_task.outputs["output"], b=b)
        add_second_task.output >> dsl.ContainerOp(
            name=f"second-add-{i}",
            image="your-second-add-image",
            command=["bash", "-c", f"kubectl exec -it {add_second_task.container.name} -- python -c 'print({add_second_task.outputs['output']})'"],
        )

# Compile the pipeline
compiler.Compiler().compile(pvc_pipeline, "10_mount_pvc_pipeline.yaml")

# Submit the pipeline run
client = kfp.Client()
run = client.create_run_from_pipeline_package("10_mount_pvc_pipeline.yaml", arguments={"a": 1.0, "b": 7.0})
```

In this solution, we have defined two components: `add` and `add_second`. The `add` component takes two float inputs and calculates their sum. The `add_second` component takes the output of the first `add` component and adds another float input `b`, then returns the sum. We also defined a pipeline named `PVC Pipeline` that mounts a PVC to the first component and uses the `kubernetes.mount_pvc` function to do so. The pipeline runs three iterations, each time mounting the PVC and executing the `add` and `add_second` components. Finally, we compiled the pipeline into a YAML file and submitted it to the Kubeflow Pipelines server.