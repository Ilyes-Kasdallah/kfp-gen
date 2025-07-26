import kfp
from kfp.dsl import pipeline, component

# Define the pipeline function name
test_one_pod_pipeline_generator = "test_one_pod_pipeline_generator"


# Define the pipeline components
@component
def transform_data(param1: float, param2: int, param3: str) -> str:
    """
    This function takes three parameters and returns a transformed string.

    Args:
    param1 (float): The first parameter.
    param2 (int): The second parameter.
    param3 (str): The third parameter.

    Returns:
    str: The transformed string.
    """
    # Perform some data transformation
    transformed_string = f"Transformed: {param1} * {param2} + {param3}"
    return transformed_string


# Define the pipeline
@pipeline(name=test_one_pod_pipeline_generator)
def pipeline():
    """
    This pipeline performs a single data transformation operation.
    """
    # Call the transform_data component with provided parameters
    result = transform_data(param1=5, param2=3, param3="Hello")
    print(result)


# Run the pipeline
if __name__ == "__main__":
    pipeline()
