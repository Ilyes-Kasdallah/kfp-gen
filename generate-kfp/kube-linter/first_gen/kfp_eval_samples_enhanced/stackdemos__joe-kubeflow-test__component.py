from kfp import pipeline
from kfp.dsl import component


@component
def download_artifact(url: str, download_to: str):
    """
    Downloads a file from a given URL to a specified location.

    Args:
    url (str): The URL of the file to download.
    download_to (str): The location where the file should be saved.

    Returns:
    None
    """
    # Use curl to download the file
    import subprocess

    subprocess.run(["curl", "-O", url, download_to])


@pipeline(name="my_pipeline")
def my_pipeline():
    """
    A pipeline that downloads an artifact from a URL and saves it to a specified location.
    """
    # Download the artifact
    download_artifact("https://example.com/data.csv", "data.csv")


# Run the pipeline
my_pipeline()
