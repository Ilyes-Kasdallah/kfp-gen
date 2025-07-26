from kfp import components
from kfp.dsl import pipeline


@pipeline(name="hello-world-pipeline")
def hello_world_pipeline():
    # Define the component 'hello' with a single argument 'message'
    hello = components.Component(
        name="hello",
        inputs={"message": components.InputType(type=str)},
        outputs={"output": components.OutputType(type=str)},
        steps=[
            components.Step(
                name="print_message",
                inputs={"message": components.InputType(type=str)},
                outputs={"output": components.OutputType(type=str)},
                code='print("Hello, {message}!")',
            )
        ],
    )

    # Return the pipeline
    return hello
