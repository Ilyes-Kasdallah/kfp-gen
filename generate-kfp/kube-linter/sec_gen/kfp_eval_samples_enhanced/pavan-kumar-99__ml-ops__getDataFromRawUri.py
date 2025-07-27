import requests
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@dsl.component
def getDataFromRawUri(uri: str) -> requests.Response:
    """
    Retrieves raw data from a specified URI using the requests library.

    Args:
    uri (str): The URI from which to retrieve the data.

    Returns:
    requests.Response: The raw data retrieved from the URI.
    """
    response = requests.get(uri)
    return response


@dsl.pipeline(name="getDataFromRawUri")
def getDataFromRawUri():
    # Define the input dataset
    dataset = Dataset(type="raw", uri="https://example.com/data.csv")

    # Define the output model
    model = Model(
        type="mlp", input_columns=["feature1", "feature2"], output_column="prediction"
    )

    # Define the pipeline steps
    get_raw_data = GetDataFromRawUri(uri=dataset.uri)

    # Define the pipeline execution
    pipeline_execution = get_raw_data()

    # Return the pipeline execution
    return pipeline_execution
