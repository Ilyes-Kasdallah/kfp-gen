import kfp
from kfp.dsl import pipeline, component


# Define the legacy_data_passing function
@component
def legacy_data_passing(data):
    # Simulate data passing logic
    if data == "constant_value":
        return "Constant Value"
    elif data == "pipeline_param":
        return "Pipeline Parameter"
    else:
        return "Component Output"


# Define the data_passing_pipeline function
@pipeline(name="data_passing_pipeline")
def data_passing_pipeline():
    # Scenario 1: Constant value
    data1 = legacy_data_passing("constant_value")
    print(f"Scenario 1: Data Passed: {data1}")

    # Scenario 2: Pipeline parameter
    data2 = legacy_data_passing("pipeline_param")
    print(f"Scenario 2: Data Passed: {data2}")

    # Scenario 3: Component output
    data3 = legacy_data_passing("Component Output")
    print(f"Scenario 3: Data Passed: {data3}")

    # Scenario 4: Constant value
    data4 = legacy_data_passing("constant_value")
    print(f"Scenario 4: Data Passed: {data4}")

    # Scenario 5: Pipeline parameter
    data5 = legacy_data_passing("pipeline_param")
    print(f"Scenario 5: Data Passed: {data5}")

    # Scenario 6: Component output
    data6 = legacy_data_passing("Component Output")
    print(f"Scenario 6: Data Passed: {data6}")


# Run the pipeline
if __name__ == "__main__":
    data_passing_pipeline()
