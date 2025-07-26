
from kfp import dsl

@dsl.pipeline(name="container-pipeline")
def container_pipeline(a=1.0, b=7.0):
    # Define the add component
    add = dsl.component(
        name="add",
        image="quay.io/rhiap/kubeflow-example:latest",
        command=["python", "components/add"],
        arguments=[
            "--a", str(a),
            "--b", str(b)
        ]
    )

    # Define the pipeline
    return add
