from kfp import pipeline
from kfp.dsl import component
from kfp.components import get_data


@pipeline(name="demo_pipeline")
def demo():
    # Step 1: Get data from 'data_source'
    data = get_data(data_source="demo_data")

    # Step 2: Process the data
    processed_data = data.upper()

    # Step 3: Return the processed data
    return processed_data


# Define the parameters for the pipeline
job_params = {"data_source": "example_data"}

# Run the pipeline
demo()
