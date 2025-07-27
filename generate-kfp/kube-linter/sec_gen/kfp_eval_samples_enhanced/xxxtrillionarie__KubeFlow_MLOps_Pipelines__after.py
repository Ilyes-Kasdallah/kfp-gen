import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Define the first component
    @component(
        name="Print Text",
        inputs=[
            Input("text", type=InputTypes.STRING),
        ],
        outputs=[
            Output("output", type=OutputTypes.STRING),
        ],
        after=["Print Text"],
    )
    def print_text(text):
        print(text)

    # Define the second component
    @component(
        name="Print Another Text",
        inputs=[
            Input("text", type=InputTypes.STRING),
        ],
        outputs=[
            Output("output", type=OutputTypes.STRING),
        ],
        after=["Print Text"],
    )
    def print_another_text(text):
        print(text)

    # Define the third component
    @component(
        name="Print Third Text",
        inputs=[
            Input("text", type=InputTypes.STRING),
        ],
        outputs=[
            Output("output", type=OutputTypes.STRING),
        ],
        after=["Print Text"],
    )
    def print_third_text(text):
        print(text)


# Run the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
kfp.compiler.Compiler().compile(pipeline_with_after, pipeline_root)
