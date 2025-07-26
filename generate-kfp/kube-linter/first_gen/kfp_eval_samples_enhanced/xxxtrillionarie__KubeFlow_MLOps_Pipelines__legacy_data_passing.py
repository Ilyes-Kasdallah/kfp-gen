import kfp
from kfp.dsl import pipeline, component


# Define the legacy_data_passing function
@component
def legacy_data_passing():
    # Write "produce_anything" to an output file path
    with open("output.txt", "w") as f:
        f.write("produce_anything")


# Define the data_passing_pipeline function
@pipeline(name="data_passing_pipeline")
def data_passing_pipeline():
    # Create three producer components
    producer_1 = legacy_data_passing()
    producer_2 = legacy_data_passing()
    producer_3 = legacy_data_passing()

    # Define the pipeline parameters
    param1 = "value1"
    param2 = "value2"

    # Define the pipeline steps
    step1 = producer_1()
    step2 = producer_2()
    step3 = producer_3()

    # Define the pipeline execution
    return step1 + step2 + step3


# Run the pipeline
if __name__ == "__main__":
    data_passing_pipeline().execute()
