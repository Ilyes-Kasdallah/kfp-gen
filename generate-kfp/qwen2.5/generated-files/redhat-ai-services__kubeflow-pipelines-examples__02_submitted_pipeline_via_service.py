
from kfp import dsl

@dsl.pipeline(name="add_pipeline")
def add_pipeline(a, b):
    # Define the base image for the component
    base_image = "image-registry.openshift-image-registry.svc:5000/openshift/python:latest"
    
    # Define the component
    @dsl.component(
        label="Add",
        inputs={
            "a": dsl.Input(type=float),
            "b": dsl.Input(type=float)
        },
        outputs={
            "result": dsl.Output(type=float)
        }
    )
    def add(a, b):
        return a + b
    
    # Execute the component
    result = add(a, b)
    
    # Return the result
    return result

# Example usage of the pipeline
if __name__ == "__main__":
    add_pipeline(3.5, 4.2).execute()
