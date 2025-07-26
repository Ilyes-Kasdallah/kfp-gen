from kfp import pipeline, component
import requests
import hashlib


@component
def download_artifact(url: str, expected_md5_checksum: str) -> str:
    """
    Downloads a file from a given URL using curl.

    Args:
    url (str): The URL of the file to download.
    expected_md5_checksum (str): The expected MD5 checksum of the downloaded file.

    Returns:
    str: The local path where the file was downloaded.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")

    # Calculate the MD5 checksum of the downloaded file
    md5_hash = hashlib.md5(response.content).hexdigest()

    # Check if the calculated MD5 matches the expected checksum
    if md5_hash != expected_md5_checksum:
        raise Exception(
            f"MD5 checksum does not match: {md5_hash} != {expected_md5_checksum}"
        )

    # Save the downloaded file to the local path
    with open("downloaded_file", "wb") as f:
        f.write(response.content)

    return "downloaded_file"


@pipeline(name="my_data_pipeline")
def my_data_pipeline():
    """
    A pipeline that downloads a file from a given URL and checks its MD5 checksum.
    """
    download_artifact("https://example.com/data.txt", "expected_md5_checksum")


if __name__ == "__main__":
    my_data_pipeline()
