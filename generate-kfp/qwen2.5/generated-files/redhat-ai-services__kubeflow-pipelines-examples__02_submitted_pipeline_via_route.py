
from kfp import dsl

@dsl.pipeline(name="add_pipeline")
def add_pipeline(a=4.0):
    # Define the add component
    @dsl.component(
        name="add",
        image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest"
    )
    def add(a, b):
        return a + b

    # Call the add component with the provided parameter
    result = add(a, b)
    return result
