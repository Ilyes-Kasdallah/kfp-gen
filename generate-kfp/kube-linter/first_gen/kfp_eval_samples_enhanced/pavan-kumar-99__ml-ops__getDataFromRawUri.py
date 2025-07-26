import requests
from kfp import components
from kfp.dsl import pipeline


@pipeline(name="getDataFromRawUri")
def getDataFromRawUri():
    # Define the GetRawData component
    @components.component(
        name="GetRawData",
        description="Retrieves raw data from a specified URI.",
        inputs={
            "uri": components.inputs.string(),
        },
        outputs={
            "raw_data": components.outputs.string(),
        },
    )
    def get_raw_data(uri):
        # Send a GET request to the specified URI
        response = requests.get(uri)
        # Return the raw data
        return response.text


# Example usage of the pipeline
if __name__ == "__main__":
    # Call the GetDataFromRawUri function
    result = getDataFromRawUri()
    print(result)
