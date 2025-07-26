from kfp import components
from kfp.dsl import pipeline


@pipeline(name="echo-pipeline")
def test_pipelines():
    # Define the echo component
    @components.component(
        name="echo",
        description="Echoes a message to the console.",
        parameters={
            "no_default_param": components.Parameter(default=0),
            "int_param": components.Parameter(default=1),
            "float_param": components.Parameter(default=1.5),
            "str_param": components.Parameter(default="string_value"),
        },
        outputs={
            "output": components.OutputType(type=str),
        },
    )
    def echo(message):
        return f"Echoing: {message}"


# Run the pipeline
test_pipelines()
