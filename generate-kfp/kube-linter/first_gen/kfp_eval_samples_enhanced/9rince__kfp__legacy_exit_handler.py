from kfp import pipeline
from kfp.dsl import component
from google.cloud import storage


@component
def legacy_exit_handler():
    # Define the GCS URL to download
    gcs_url = "gs://your-bucket-name/path/to/your/file.txt"

    # Download the file from GCS
    gsutil.download(gcs_url, "downloaded_file.txt")

    # Echo the downloaded file
    print("File downloaded successfully!")


@pipeline(name="Exit Handler Pipeline")
def exit_handler_pipeline():
    # Call the legacy_exit_handler component
    legacy_exit_handler()


# Run the pipeline
exit_handler_pipeline()
