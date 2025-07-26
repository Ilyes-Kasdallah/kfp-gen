
from kfp import dsl

@dsl.pipeline(name="echo-pipeline")
def test_pipelines():
    # Define the components
    echo = dsl.component(
        name="echo",
        description="Echoes the input values.",
        parameters={
            "no_default_param": dsl.int_param(default=0),
            "int_param": dsl.int_param(default=1),
            "float_param": dsl.float_param(default=1.5),
            "str_param": dsl.string_param(default="string_value")
        },
        operations=[
            dsl.output("output", dsl.string())
        ]
    )

    # Execute the pipeline
    echo.execute()
