
from kfp import pipeline
from kfp.components import parameter_with_format_test

@pipeline(name="my_pipeline")
def my_pipeline():
    # Define a parameter with format test
    param = parameter_with_format_test("param_name", "string")

    # Process the parameter
    processed_param = f"Processed {param}"

    return processed_param

# Example usage
result = my_pipeline()
print(result)
