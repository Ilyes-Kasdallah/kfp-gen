from kfp import pipeline
from kfp.dsl import component
import requests
import hashlib


@component
def download_artifact(url: str, expected_md5_checksum: str) -> str:
    """
    Downloads a file from a URL and verifies its MD5 checksum.

    Args:
    url (str): The URL of the file to download.
    expected_md5_checksum (str): The expected MD5 checksum of the downloaded file.

    Returns:
    str: The path to the downloaded file.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")

    # Calculate the MD5 checksum of the downloaded file
    md5_hash = hashlib.md5(response.content).hexdigest()

    # Check if the calculated checksum matches the expected checksum
    if md5_hash != expected_md5_checksum:
        raise Exception(
            f"MD5 checksum mismatch: expected {expected_md5_checksum}, got {md5_hash}"
        )

    # Return the path to the downloaded file
    return response.url


@pipeline(name="my_pipeline")
def my_pipeline():
    """
    A pipeline that downloads a file from a URL and then trains a model.
    """
    download_artifact("https://example.com/data.csv", "1234567890abcdef")
    # Add more components here as needed


# Run the pipeline
my_pipeline()
