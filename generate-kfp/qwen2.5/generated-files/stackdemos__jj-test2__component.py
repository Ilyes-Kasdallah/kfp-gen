
from kfp import dsl

@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Define the download-artifact component
    @dsl.component
    def download_artifact(url, download_to):
        # Use curl to download the artifact
        import subprocess
        subprocess.run(['curl', '-O', url, download_to], check=True)

# Example usage
download_artifact('https://example.com/data.csv', '/path/to/save/data.csv')
