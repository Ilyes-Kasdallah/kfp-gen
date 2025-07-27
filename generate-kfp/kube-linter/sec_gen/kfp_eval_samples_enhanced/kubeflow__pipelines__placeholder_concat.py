import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the placeholder_concat function
@component
def placeholder_concat(input_one: str, input_two: str) -> str:
    # Concatenate the inputs with a '+'
    concatenated_string = input_one + "+" + input_two
    # Return the concatenated string
    return concatenated_string


# Define the pipeline
@pipeline(name="one-step-pipeline-with-concat-placeholder")
def one_step_pipeline_with_concat_placeholder():
    # Call the placeholder_concat function with two string inputs
    result = placeholder_concat("Hello", "World")
    # Output the result
    Output(result)


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(one_step_pipeline_with_concat_placeholder)
