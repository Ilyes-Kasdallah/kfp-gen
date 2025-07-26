from kfp import pipeline
from kfp.dsl import component

# Import necessary modules
from kfp.components import lightweight_python_functions_v2_with_outputs


@dsl.pipeline(name="functions-with-outputs")
def functions_with_outputs():
    # Define the first component: concat_message
    concat_message = component(
        name="concat_message",
        description="Concatenates two strings and returns a single string.",
        inputs={
            "first": component.input_type(str),
            "second": component.input_type(str),
        },
        outputs={"result": component.output_type(str)},
        steps=[
            component.step(
                name="concatenate_strings",
                code=lightweight_python_functions_v2_with_outputs.concat_strings,
                inputs={
                    "first": component.input_type(str),
                    "second": component.input_type(str),
                },
                outputs={"result": component.output_type(str)},
            )
        ],
    )

    # Define the second component: add_numbers
    add_numbers = component(
        name="add_numbers",
        description="Adds two numbers and returns a single integer.",
        inputs={"num1": component.input_type(int), "num2": component.input_type(int)},
        outputs={"result": component.output_type(int)},
        steps=[
            component.step(
                name="add_numbers",
                code=lightweight_python_functions_v2_with_outputs.add_numbers,
                inputs={
                    "num1": component.input_type(int),
                    "num2": component.input_type(int),
                },
                outputs={"result": component.output_type(int)},
            )
        ],
    )

    # Define the third component: create_artifact
    create_artifact = component(
        name="create_artifact",
        description="Creates an artifact with a given message.",
        inputs={"message": component.input_type(str)},
        outputs={"artifact": component.output_type(str)},
        steps=[
            component.step(
                name="create_artifact",
                code=lightweight_python_functions_v2_with_outputs.create_artifact,
                inputs={"message": component.input_type(str)},
                outputs={"artifact": component.output_type(str)},
            )
        ],
    )

    # Define the fourth component: main
    main = component(
        name="main",
        description=" orchestrates the execution of the pipeline.",
        inputs={
            "concat_message": component.input_type(str),
            "add_numbers": component.input_type(int),
            "create_artifact": component.input_type(str),
        },
        outputs={"output": component.output_type(str)},
        steps=[
            component.step(
                name="concatenate_message",
                code=concat_message.code,
                inputs={
                    "first": concat_message.inputs["first"],
                    "second": concat_message.inputs["second"],
                },
                outputs={"result": concat_message.outputs["result"]},
            ),
            component.step(
                name="add_numbers",
                code=add_numbers.code,
                inputs={
                    "num1": add_numbers.inputs["num1"],
                    "num2": add_numbers.inputs["num2"],
                },
                outputs={"result": add_numbers.outputs["result"]},
            ),
            component.step(
                name="create_artifact",
                code=create_artifact.code,
                inputs={"message": create_artifact.inputs["message"]},
                outputs={"artifact": create_artifact.outputs["artifact"]},
            ),
            component.step(
                name="main",
                code=main.code,
                inputs={
                    "concat_message": concat_message.inputs["result"],
                    "add_numbers": add_numbers.inputs["result"],
                    "create_artifact": create_artifact.inputs["artifact"],
                },
                outputs={"output": main.outputs["output"]},
            ),
        ],
    )

    return main


# Run the pipeline
if __name__ == "__main__":
    main()
