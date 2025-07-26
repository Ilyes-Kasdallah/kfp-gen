from kfp import pipeline
from kfp.dsl import component


@component
def download_artifact(url: str, download_to: str, md5sum: str) -> None:
    """
    Downloads a file from a URL using curl and checks its MD5 checksum.

    Args:
    url (str): The URL of the file to download.
    download_to (str): The local path where the file will be saved.
    md5sum (str): The MD5 checksum of the file to verify.
    """
    # Use curl to download the file
    import subprocess

    subprocess.run(["curl", "-O", url], check=True)

    # Check if the downloaded file has the correct MD5 checksum
    import hashlib

    with open(download_to, "rb") as f:
        content = f.read()
        expected_md5 = hashlib.md5(content).hexdigest()
        assert (
            expected_md5 == md5sum
        ), f"MD5 checksum does not match: expected {expected_md5}, got {content}"


# Define the pipeline
with pipeline("my_pipeline") as p:
    # Download an artifact
    p.download_artifact(
        url="https://example.com/data.csv",
        download_to="/path/to/downloaded/file.csv",
        md5sum="e3b292f0c74d816a0999999999999999",
    )
