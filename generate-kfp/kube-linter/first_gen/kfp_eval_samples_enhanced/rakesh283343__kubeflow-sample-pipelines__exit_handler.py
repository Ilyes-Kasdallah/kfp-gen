from kfp import pipeline
from kfp.dsl import component


@component
def download_file(url: str = "gs://ml-pipeline/shakespeare/shakespeare1.txt"):
    """
    Downloads a text file from a Google Cloud Storage (GCS) URL.

    Args:
    url (str): The URL of the GCS file to download.

    Returns:
    str: The content of the downloaded file.
    """
    # Import necessary modules
    import gsutil

    # Download the file
    gsutil.download(url, "downloaded_file.txt")

    # Return the content of the downloaded file
    return open("downloaded_file.txt", "r").read()


@pipeline(name="Exit Handler")
def exit_handler():
    """
    A simple pipeline that demonstrates the use of an exit handler.

    Returns:
    None
    """
    # Call the download_file function
    content = download_file()

    # Print the content
    print(content)


# Run the pipeline
exit_handler()
