
from kfp import dsl

@dsl.pipeline(name="one-step-pipeline-with-concat-placeholder")
def one_step_pipeline_with_concat_placeholder():
    # Define the components
    component1 = dsl.component(
        name="Component with concat placeholder",
        description="Concatenates two strings with a '+' symbol and '=' three",
        inputs=[
            dsl.input("input_one", type="string"),
            dsl.input("input_two", type="string")
        ],
        outputs={
            "concat_result": dsl.output("concat_result", type="string")
        },
        steps=[
            dsl.step(
                name="Concatenate Strings",
                task_id="concatenate_strings",
                inputs={
                    "input_one": dsl.input("input_one"),
                    "input_two": dsl.input("input_two")
                },
                outputs={
                    "concat_result": dsl.output("concat_result", type="string")
                },
                body=lambda inputs: f"{inputs['input_one']}+{inputs['input_two']}=three"
            )
        ]
    )

    # Define the pipeline function
    return component1
