
from kfp import dsl

@dsl.pipeline(name="lightweight_python_functions_v2_with_outputs")
def lightweight_python_functions_v2_with_outputs():
    # First component: Generates two strings and outputs them to an intermediate artifact
    first_component = dsl.component(
        name="first_component",
        description="Generates two strings and outputs them to an intermediate artifact",
        steps=[
            dsl.output("output_string1", type=str),
            dsl.output("output_string2", type=str)
        ]
    )

    # Second component: Performs some operations on the output of the first component
    second_component = dsl.component(
        name="second_component",
        description="Performs some operations on the output of the first component",
        steps=[
            dsl.input("input_string1", type=str),
            dsl.input("input_string2", type=str),
            dsl.output("result", type=str)
        ]
    )

    # Third component: Aggregates the results from the second component
    third_component = dsl.component(
        name="third_component",
        description="Aggregates the results from the second component",
        steps=[
            dsl.input("result1", type=str),
            dsl.input("result2", type=str),
            dsl.output("final_result", type=str)
        ]
    )

    # Pipeline execution
    return first_component + second_component + third_component

# Function to test the pipeline
@dsl.pipeline_test(name="lightweight_python_functions_v2_with_outputs_test")
def lightweight_python_functions_v2_with_outputs_test():
    result = lightweight_python_functions_v2_with_outputs()
    assert result == "firstsecondresult"
