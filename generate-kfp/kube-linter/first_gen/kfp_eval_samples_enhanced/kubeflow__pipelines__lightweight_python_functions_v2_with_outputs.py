from kfp import pipeline
from kfp.dsl import component

# Import necessary modules
from kfp.components import lightweight_python_functions_v2_with_outputs


# Define the pipeline
@pipeline(name="functions-with-outputs")
def functions_with_outputs():
    # Define the first component: concat_message
    concat_message = component(
        name="concat_message",
        description="Concatenates two strings and returns the result.",
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

    # Define the second component: add_integers
    add_integers = component(
        name="add_integers",
        description="Adds two integers and returns the result.",
        inputs={"a": component.input_type(int), "b": component.input_type(int)},
        outputs={"result": component.output_type(int)},
        steps=[
            component.step(
                name="add_numbers",
                code=lightweight_python_functions_v2_with_outputs.add_numbers,
                inputs={"a": component.input_type(int), "b": component.input_type(int)},
                outputs={"result": component.output_type(int)},
            )
        ],
    )

    # Define the third component: create_artifact
    create_artifact = component(
        name="create_artifact",
        description="Creates an artifact with a given message.",
        inputs={"message": component.input_type(str)},
        outputs={"artifact": component.output_type(kfp.artifact.Artifact)},
        steps=[
            component.step(
                name="create_artifact",
                code=lightweight_python_functions_v2_with_outputs.create_artifact,
                inputs={"message": component.input_type(str)},
                outputs={"artifact": component.output_type(kfp.artifact.Artifact)},
            )
        ],
    )

    # Define the fourth component: main
    main = component(
        name="main",
        description=" orchestrates the pipeline execution.",
        inputs={
            "concat_result": component.input_type(str),
            "add_result": component.input_type(int),
            "artifact": component.input_type(kfp.artifact.Artifact),
        },
        outputs={"final_output": component.output_type(str)},
        steps=[
            component.step(
                name="process_data",
                code=lightweight_python_functions_v2_with_outputs.process_data,
                inputs={
                    "concat_result": component.input_type(str),
                    "add_result": component.input_type(int),
                    "artifact": component.input_type(kfp.artifact.Artifact),
                },
                outputs={"final_output": component.output_type(str)},
            )
        ],
    )

    # Return the main component
    return main


# Execute the pipeline
if __name__ == "__main__":
    from kfp import sdk

    sdk.init()
    result = functions_with_outputs().execute()
    print(result)
