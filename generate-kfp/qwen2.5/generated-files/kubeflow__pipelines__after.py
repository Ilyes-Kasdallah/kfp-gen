
from kfp import dsl

@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Define the first task using PrintText
    @dsl.component(name="Print Text")
    def print_text(text):
        print(text)

    # Define the second task using PrintText
    @dsl.component(name="Print Text")
    def print_text2(text):
        print(text)

    # Define the third task using PrintText
    @dsl.component(name="Print Text")
    def print_text3(text):
        print(text)

    # Use after to execute the third task after the second task
    print_text3.after(print_text2)

# Execute the pipeline
pipeline_with_after()
