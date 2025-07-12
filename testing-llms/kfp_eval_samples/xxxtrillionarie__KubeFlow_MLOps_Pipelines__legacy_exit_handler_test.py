```python
from kfp import dsl
import requests

# Define the download_and_print component
@dsl.component(
    base_image='python:3.8',
    packages_to_install=['requests'],
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.TEXT)
)
def download_and_print(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
    else:
        raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")

# Define the main pipeline
@dsl.pipeline(name="download_and_print")
def legacy_exit_handler_test():
    url = "https://example.com/sample.txt"
    download_and_print(url)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(legacy_exit_handler_test, 'legacy_exit_handler_test.yaml')
```

In this solution, we define a `download_and_print` component that takes a URL as input, downloads the file using the `requests` library, and prints its contents to the standard output. We also define a main pipeline named `legacy_exit_handler_test` that calls the `download_and_print` component with a sample URL. Finally, we compile the pipeline into a YAML file using the `kfp.compiler.Compiler()` class.