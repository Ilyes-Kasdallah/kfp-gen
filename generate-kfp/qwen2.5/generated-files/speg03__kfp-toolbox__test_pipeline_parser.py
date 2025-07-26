
from kfp import dsl

@dsl.pipeline(name="echo-pipeline")
def echo_pipeline():
    # Define a component that echoes a message
    @dsl.component
    def echo_component(message):
        return f"Echo: {message}"

# Create a pipeline that uses the echo_component
@dsl.pipeline(name="test_pipeline_parser")
def test_pipeline_parser():
    # Use the echo_component in the pipeline
    echo_component("Hello, World!")
