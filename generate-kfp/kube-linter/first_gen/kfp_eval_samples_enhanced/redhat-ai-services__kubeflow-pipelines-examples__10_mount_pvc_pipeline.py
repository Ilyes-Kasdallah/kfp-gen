from kfp import pipeline
from kfp.dsl import component


@component
def add(a: float, b: float) -> float:
    """Add two floats."""
    return a + b


@component
def mount_pvc(pvc_name: str) -> None:
    """Mount a Persistent Volume Claim."""
    # This is a placeholder for actual PVC mounting logic
    print(f"Mounting PVC {pvc_name} to /opt/data")


@pipeline(name="PVC Pipeline")
def one_addition_pipeline():
    """Two addition steps using Kubeflow Pipelines."""
    result = add(5.0, 4.0)
    mount_pvc("my-data")
    print(f"The result of adding 5.0 and 4.0 is: {result}")


# Run the pipeline
one_addition_pipeline()
