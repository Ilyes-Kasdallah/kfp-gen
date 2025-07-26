from kfp import pipeline, component
from kfp.dsl import Input, Output

# Import necessary modules
from kfp.components import lightweight_python_functions_v2_with_outputs


# Define the pipeline
@pipeline(name="functions-with-outputs")
def functions_with_outputs():
    # Define the first component
    concat_message = component.Component(
        name="concat_message",
        inputs=[
            Input("first", type=InputType.STRING),
            Input("second", type=InputType.STRING),
        ],
        outputs=[Output("result", type=OutputType.STRING)],
        steps=[
            component.Step(
                name="concatenate_strings",
                code=lightweight_python_functions_v2_with_outputs.concat_strings,
                inputs={"first": "Hello", "second": "World"},
                outputs={"result": "HelloWorld"},
            )
        ],
    )

    # Define the second component
    add_numbers = component.Component(
        name="add_numbers",
        inputs=[Input("num1", type=InputType.INT), Input("num2", type=InputType.INT)],
        outputs=[Output("sum", type=OutputType.INT)],
        steps=[
            component.Step(
                name="calculate_sum",
                code=lightweight_python_functions_v2_with_outputs.calculate_sum,
                inputs={"num1": 5, "num2": 3},
                outputs={"sum": 8},
            )
        ],
    )

    # Define the third component
    create_artifact = component.Component(
        name="create_artifact",
        inputs=[Input("message", type=InputType.STRING)],
        outputs=[Output("artifact_name", type=OutputType.STRING)],
        steps=[
            component.Step(
                name="create_artifact",
                code=lightweight_python_functions_v2_with_outputs.create_artifact,
                inputs={"message": "Hello from Kubeflow"},
                outputs={"artifact_name": "kubeflow_output"},
            )
        ],
    )

    # Define the fourth component
    return (
        concatenate_message(
            concat_message.inputs["first"], concat_message.inputs["second"]
        )
        + add_numbers(add_numbers.inputs["num1"], add_numbers.inputs["num2"])
        + create_artifact(create_artifact.inputs["message"])
    )


# Run the pipeline
functions_with_outputs()
