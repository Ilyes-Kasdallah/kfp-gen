
from kfp import dsl

@dsl.pipeline(name="getDataFromRawUri")
def getDataFromRawUri():
    # Define the GetRawData component
    @dsl.component
    def get_raw_data(uri):
        # Use requests to fetch data from the specified URI
        response = requests.get(uri)
        return response.text

# Example usage of the GetDataFromRawUri pipeline
if __name__ == "__main__":
    # Call the GetDataFromRawUri pipeline
    result = getDataFromRawUri()
    print(result)
