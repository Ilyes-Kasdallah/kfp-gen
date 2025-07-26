import kfp
from kfp.dsl import pipeline, component


@component
def download_and_print(url):
    """Download a file from the specified URL and print its contents."""
    # Simulate downloading the file
    print(f"Downloading file from {url}")
    # Simulate printing the contents of the downloaded file
    print("File content:")
    with open(url, "r") as file:
        for line in file:
            print(line.strip())


@pipeline(name="download_and_print_pipeline")
def download_and_print_pipeline():
    """Pipeline to download and print a file."""
    download_and_print("https://example.com/file.txt")


# Run the pipeline
if __name__ == "__main__":
    download_and_print_pipeline()
