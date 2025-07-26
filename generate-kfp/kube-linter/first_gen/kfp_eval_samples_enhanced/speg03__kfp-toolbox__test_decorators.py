from kfp import components
from kfp.dsl import pipeline


@pipeline(name="echo-pipeline")
def test_decorators():
    # Define the echo component
    @components.component(
        name="echo",
        description="This component takes no input and returns the string 'hello, world'.",
    )
    def echo():
        return "hello, world"


# Run the pipeline
test_decorators()
