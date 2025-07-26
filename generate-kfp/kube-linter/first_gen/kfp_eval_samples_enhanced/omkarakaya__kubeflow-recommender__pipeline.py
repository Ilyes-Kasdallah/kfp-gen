from kfp import pipeline
from kfp.dsl import component


@component
def create_pvc(pvc_name: str, pvc_size: int, pvc_mode: str) -> None:
    """
    Creates a PersistentVolumeClaim (PVC) named 'my-pvc' with a size of 1Gi and ReadWriteOnce (RWO) mode.

    Args:
    pvc_name (str): The name of the PVC.
    pvc_size (int): The size of the PVC in Gi.
    pvc_mode (str): The mode of the PVC (e.g., RWO).
    """
    # Create a PersistentVolumeClaim
    from kfp.core import resources
    from kfp.core import volume
    from kfp.core import deployment
    from kfp.core import pipeline
    from kfp.core import component

    # Define the PVC
    pvc = volume.PersistentVolumeClaim(
        name=pvc_name,
        capacity=resources.Gi(pvc_size),
        access_modes=[resources.ReadWriteOnce],
        storage_class="gp2",
    )

    # Deploy the PVC
    deployment = deployment.Deployment(
        name="create_pvc",
        steps=[
            component.ComponentStep(
                name="create_pvc",
                inputs={
                    "pvc_name": pvc_name,
                    "pvc_size": pvc_size,
                    "pvc_mode": pvc_mode,
                },
                outputs={"pvc": pvc},
            )
        ],
    )

    # Run the deployment
    pipeline.run(deployment)


# Define the pipeline
@pipeline(name="Kubeflow Pipeline Test")
def test_kubeflow_pipeline():
    create_pvc("my-pvc", 1, "RWO")


# Execute the pipeline
test_kubeflow_pipeline()
