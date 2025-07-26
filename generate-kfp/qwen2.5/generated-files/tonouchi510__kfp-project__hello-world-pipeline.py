
from kfp import pipeline
from kfp.components import component

@component
def hello(message):
    return f"Hello, {message}!"

@pipeline(name="hello-world-pipeline")
def hello_world_pipeline():
    return hello("World")

# Example usage:
result = hello_world_pipeline()
print(result)
