
from kfp import pipeline
from kfp.components import create_pvc

@dsl.pipeline(name="Kubeflow Pipeline Test")
def Kubeflow_Pipeline_Test():
    # Create a PersistentVolumeClaim (PVC) named "my-pvc" with a size of 1Gi and ReadWriteOnce (RWO) mode
    create_pvc(
        name="my-pvc",
        storage_class="standard",
        access_mode="ReadWriteOnce",
        size="1Gi"
    )
