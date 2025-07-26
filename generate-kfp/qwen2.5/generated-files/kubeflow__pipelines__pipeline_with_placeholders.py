
from kfp import dsl

@dsl.pipeline(name="pipeline-with-placeholders")
def pipeline_with_placeholders():
    # Define the single component
    print_all_placeholders = dsl.component(
        name="print_all_placeholders",
        description="Prints all placeholders in the pipeline execution.",
        inputs=[
            dsl.input(name="job_name", type="string"),
        ],
        outputs=[],
        steps=[
            dsl.task(
                name="print_placeholder",
                description="Prints the value of the placeholder.",
                inputs={
                    "placeholder": dsl.input(name="placeholder", type="string"),
                },
                outputs=[],
                steps=[
                    dsl.output(name="output", type="string"),
                ],
            ),
        ],
    )

    # Return the pipeline
    return print_all_placeholders
