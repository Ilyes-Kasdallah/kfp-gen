```python
import kfp
from kfp import dsl
from kfp.components import create_component_from_func

# Define the GetRawData component
def get_raw_data(uri):
    import requests
    response = requests.get(uri)
    return response

get_raw_data_op = create_component_from_func(
    func=get_raw_data,
    base_image="python:slim",
    package_path="./components/getRawData.yaml"
)

# Define the getDataFromRawUri pipeline
@dsl.pipeline(name="getDataFromRawUri")
def getDataFromRawUri(raw_uri):
    # Call the GetRawData component
    raw_data = get_raw_data_op(raw_uri=raw_uri)

# Compile the pipeline
compiler.Compiler().compile(getDataFromRawUri, "getDataFromRawUri.yaml")

# Submit the pipeline run
client = kfp.Client()
run = client.run_pipeline("your-pipeline-id", "getDataFromRawUri.yaml", {"raw_uri": "http://example.com/data.csv"})
```

In this solution, we define a `GetRawData` component that uses the `requests` library to retrieve data from a given URI. We then use this component within a `getDataFromRawUri` pipeline, which simply calls the `GetRawData` component with a specified URI. Finally, we compile the pipeline and submit it for execution.