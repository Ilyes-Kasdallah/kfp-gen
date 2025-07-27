import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="echo-pipeline")
def test_pipelines():
    # Define the echo component
    @component
    def echo(
        no_default_param: int = 0,
        int_param: int = 1,
        float_param: float = 1.5,
        str_param: str = "string_value",
    ):
        # Print the input parameters
        print(
            f"Input Parameters: {no_default_param}, {int_param}, {float_param}, {str_param}"
        )
        # Return the output
        return f"Echoed: {no_default_param} + {int_param} + {float_param} + {str_param}"


# Run the pipeline
test_pipelines()
