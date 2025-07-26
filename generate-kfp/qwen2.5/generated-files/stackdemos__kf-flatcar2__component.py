
from kfp import dsl

@dsl.pipeline(name="my-pipeline")
def my_pipeline():
    # Define the download-artifact component
    @dsl.component
    def download_artifact(url, download_to, md5sum):
        # Use curl to download the artifact
        import subprocess
        subprocess.run(['curl', '-o', download_to, url], check=True)
        # Check if the download was successful
        if subprocess.call(['md5sum', download_to]) == 0:
            print(f"Download successful: {download_to}")
        else:
            print(f"Download failed: {download_to}")

# Example usage
download_artifact("https://example.com/data.csv", "/path/to/downloaded/file.csv", "e3b29e9a-41c7-4d8f-ba6f-9b0b0b0b0b0b")
