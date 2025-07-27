import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="demo_pipeline")
def demo():
    # Step 1: Get data from job_params.data_source
    get_data = component(
        name="get_data",
        description='Simulates fetching data and returns a string "data"',
        inputs={
            "data_source": Input[str],
        },
        outputs={
            "data": Output[str],
        },
        base_image="job_constants.BASE_IMAGE",
    )

    # Step 2: Process the data
    process_data = component(
        name="process_data",
        description='Processes the data and returns a string "processed_data"',
        inputs={
            "data": Input[str],
        },
        outputs={
            "processed_data": Output[str],
        },
        base_image="job_constants.BASE_IMAGE",
    )

    # Step 3: Combine the processed data
    combine_data = component(
        name="combine_data",
        description="Combines the processed data into a single string",
        inputs={
            "processed_data": Input[str],
        },
        outputs={
            "combined_data": Output[str],
        },
        base_image="job_constants.BASE_IMAGE",
    )

    # Step 4: Return the combined data
    return combine_data()


# Example usage of the pipeline function
if __name__ == "__main__":
    demo()
