import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="echo-pipeline")
def test_pipeline_parser():
    # Define a simple echo operation
    @component
    def echo(input_text):
        return f"Echo: {input_text}"


# Run the pipeline
test_pipeline_parser()
