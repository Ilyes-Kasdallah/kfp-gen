import kfp
from kfp.dsl import pipeline, component


@component
def download_artifact(url: str, destination: str) -> None:
    """
    Downloads a file from a given URL to a specified location.

    Args:
    url (str): The URL of the file to download.
    destination (str): The local path where the file will be saved.
    """
    # Use curl to download the file
    import subprocess

    subprocess.run(["curl", "-O", url, destination], check=True)


@pipeline(name="my-data-processing-pipeline")
def process_data():
    """
    Processes data by downloading an artifact and verifying its MD5 checksum.
    """
    # Download the artifact
    download_artifact("https://example.com/data.txt", "/path/to/data.txt")

    # Verify the MD5 checksum
    import hashlib

    with open("/path/to/data.txt", "rb") as f:
        md5_hash = hashlib.md5(f.read()).hexdigest()

    # Check if the MD5 checksum matches the expected value
    assert (
        md5_hash == "expected_md5_checksum"
    ), f"Expected MD5 checksum '{expected_md5_checksum}', but got '{md5_hash}'"


if __name__ == "__main__":
    process_data()
