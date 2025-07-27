import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the reusable component
@component
def norok_reusable_compo_pipeline(input_1_uri):
    # Read the content of the input file
    with open(input_1_uri, "r") as file:
        content = file.read()

    # Process the content (for demonstration purposes, just print it)
    print(content)


# Define the pipeline
@pipeline(name="My pipeline")
def my_pipeline():
    # Call the reusable component with an input
    norok_reusable_compo_pipeline("https://www.w3.org/TR/PNG/iso_8859-1.txt")


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(my_pipeline)
