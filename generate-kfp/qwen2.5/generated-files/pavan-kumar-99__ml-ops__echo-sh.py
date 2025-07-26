
from kfp import dsl

@dsl.pipeline(name="my-pipeline")
def my_pipeline():
    # Define the component
    @dsl.component(name="echo")
    def echo_sh(input_text):
        return f"Hi {input_text}"

# Execute the pipeline
my_pipeline()
