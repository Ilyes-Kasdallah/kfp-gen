from kfp import pipeline, component
import requests
import hashlib


@component
def http_download_op(url: str, download_to: str):
    """
    Downloads a file from a given URL to a specified location using curl.

    Args:
    url (str): The URL of the file to download.
    download_to (str): The location where the file should be saved.

    Returns:
    None
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(download_to, "wb") as f:
            f.write(response.content)
        print(f"File downloaded successfully to {download_to}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


@component
def md5sum_op(file_path: str):
    """
    Calculates the MD5 checksum of a file.

    Args:
    file_path (str): The path to the file whose checksum is to be calculated.

    Returns:
    str: The MD5 checksum of the file.
    """
    with open(file_path, "rb") as f:
        md5_hash = hashlib.md5()
        while chunk := f.read(4096):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


@dsl.pipeline(name="pipeline_name_needs_to_be_specified_from_the_python_code")
def pipeline_name_needs_to_be_specified_from_the_python_code():
    """
    A pipeline that downloads a file from a given URL and calculates its MD5 checksum.
    """
    # Download the file
    http_download_op("https://example.com/file.zip", "downloaded_file.zip")

    # Calculate the MD5 checksum
    md5_checksum = md5sum_op("downloaded_file.zip")

    # Output the results
    print(f"MD5 checksum of downloaded file: {md5_checksum}")


# Run the pipeline
pipeline_name_needs_to_be_specified_from_the_python_code()
