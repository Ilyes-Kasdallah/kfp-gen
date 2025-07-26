
from kfp import dsl

@dsl.pipeline(name="pipeline")
def test_one_pod_pipeline_generator(param1: float, param2: int, param3: str):
    # Perform data transformation operations here
    transformed_data = param1 * param2 + param3
    return transformed_data

# Example usage of the pipeline
if __name__ == "__main__":
    result = test_one_pod_pipeline_generator(5, 3, "2023-04-01")
    print(result)
