
from kfp import dsl

@dsl.pipeline(name="echo-pipeline")
def echo_pipeline():
    # Define the echo component
    @dsl.component(name="echo")
    def echo():
        return "hello, world"

# Run the pipeline
echo_pipeline()
