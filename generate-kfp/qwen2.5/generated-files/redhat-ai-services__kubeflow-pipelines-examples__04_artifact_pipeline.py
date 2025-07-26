
from kfp import dsl

@dsl.pipeline(name="Artifact Pipeline")
def create_artifact():
    # Define the base image
    base_image = "image-registry.openshift-image-registry.svc:5000/openshift/python:latest"
    
    # Define the task to serialize data
    serialize_task = dsl.component(
        name="serialize_data",
        image=base_image,
        command=["python", "-m", "pickle", "data_to_serialize.pkl"]
    )
    
    # Define the task to deserialize data
    deserialize_task = dsl.component(
        name="deserialize_data",
        image=base_image,
        command=["python", "-m", "pickle", "data_deserialized.pkl"]
    )
    
    # Return the results of the tasks
    return serialize_task.result(), deserialize_task.result()
