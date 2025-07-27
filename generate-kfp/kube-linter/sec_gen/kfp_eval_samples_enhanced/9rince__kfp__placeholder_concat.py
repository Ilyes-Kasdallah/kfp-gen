import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the placeholder_concat function
@component
def placeholder_concat(input_one: str, input_two: str) -> str:
    # Concatenate the inputs with a '+'
    concatenated = input_one + "+" + input_two
    # Check if the result equals 'one+two=three'
    if concatenated == "one+two=three":
        return concatenated
    else:
        raise ValueError("The concatenated result does not match the expected output.")


# Define the pipeline
@pipeline(name="one-step-pipeline-with-concat-placeholder")
def one_step_pipeline_with_concat_placeholder():
    # Call the placeholder_concat function with two string inputs
    result = placeholder_concat("one", "two")
    # Output the result
    Output(result)


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(one_step_pipeline_with_concat_placeholder)
