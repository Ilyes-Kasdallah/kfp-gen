import kfp
from kfp.dsl import pipeline, component


# Define the pipeline
@pipeline(name="lightweight_python_functions_v2_with_outputs")
def lightweight_python_functions_v2_with_outputs():
    # Define the first component
    @component
    def first_component():
        return "first"

    # Define the second component
    @component
    def second_component():
        return "second"

    # Define the third component
    @component
    def third_component():
        return "third"

    # Define the pipeline execution
    first_output = first_component()
    second_output = second_component()
    third_output = third_component()

    # Return the results of the components
    return {"first": first_output, "second": second_output, "third": third_output}


# Run the pipeline
if __name__ == "__main__":
    lightweight_python_functions_v2_with_outputs()
