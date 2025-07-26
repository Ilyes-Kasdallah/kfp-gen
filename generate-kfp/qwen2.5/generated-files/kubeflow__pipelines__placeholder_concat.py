
from kfp import dsl

@dsl.pipeline(name="one-step-pipeline-with-concat-placeholder")
def one_step_pipeline_with_concat_placeholder(input_one, input_two):
    # Concatenate input_one and input_two with a '+' symbol and the string '=three'
    concatenated_string = f"{input_one}+{input_two}=three"
    return concatenated_string

# Example usage
result = one_step_pipeline_with_concat_placeholder("Hello", "World")
print(result)  # Output: Hello+World=three
