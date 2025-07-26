
from kfp import dsl

@dsl.pipeline(name="echo-pipeline")
def test_cli():
    # Execute the echo component once
    echo_component = dsl.component(
        name="echo",
        implementation=dsl.literal("hello, world"),
    )
    echo_component()
