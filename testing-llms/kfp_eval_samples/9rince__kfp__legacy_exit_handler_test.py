```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='download_and_print_pipeline')
def download_and_print():
    # Download a file
    @dsl.component(
        base_image='ubuntu',
        packages_to_install=['wget'],
        output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.URI)
    )
    def download_file(url: str, output_uri: dsl.OutputArtifact):
        import wget
        wget.download(url, output_uri.path)

    # Print the contents of the downloaded file
    @dsl.component(
        base_image='ubuntu',
        packages_to_install=['cat'],
        input_artifact=dsl.InputArtifact(type=dsl.ArtifactType.URI),
        output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.TEXT)
    )
    def print_contents(input_uri: dsl.InputArtifact):
        import subprocess
        result = subprocess.run(['cat', input_uri.path], capture_output=True, text=True)
        print(result.stdout)

    # Execute the pipeline
    download_file(url='https://example.com/file.txt', output_uri=print_contents.input_uri)
```

In this solution, we define a Kubeflow Pipeline named `download_and_print_pipeline` using the `@dsl.pipeline` decorator. Inside the pipeline, we use two components: `download_file` and `print_contents`.

The `download_file` component downloads a file from a specified URL and saves it to an output URI. It uses the `wget` package to perform the download.

The `print_contents` component reads the contents of the downloaded file and prints them to the console. It uses the `subprocess` module to execute the `cat` command on the file.

Finally, we execute the pipeline by calling the `download_file` component with the desired URL and passing the output URI of the `print_contents` component as an input. This setup ensures that the pipeline performs the required operations in sequence and handles the file I/O correctly.