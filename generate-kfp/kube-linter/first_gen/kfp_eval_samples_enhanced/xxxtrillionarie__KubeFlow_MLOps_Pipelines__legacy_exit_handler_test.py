import kfp
from kfp.dsl import pipeline, component


@component
def download_and_print(url: str) -> None:
    # Download the file from the URL
    with open("downloaded_file.txt", "wb") as f:
        f.write(requests.get(url).content)

    # Print the contents of the downloaded file
    print(open("downloaded_file.txt").read())


@pipeline(name="download_and_print")
def legacy_exit_handler_test():
    # Define the input parameter
    url = "https://example.com/data.txt"

    # Call the download_and_print component
    download_and_print(url)


# Run the pipeline
legacy_exit_handler_test()
