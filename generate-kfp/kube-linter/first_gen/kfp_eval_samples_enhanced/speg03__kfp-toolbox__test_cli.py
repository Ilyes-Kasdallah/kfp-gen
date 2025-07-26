from kfp import components
from kfp.dsl import pipeline


@pipeline(name="echo-pipeline")
def test_cli():
    # Define the echo component
    @components.component
    def echo():
        return "hello, world"

    # Execute the echo component
    result = echo()
    print(result)
