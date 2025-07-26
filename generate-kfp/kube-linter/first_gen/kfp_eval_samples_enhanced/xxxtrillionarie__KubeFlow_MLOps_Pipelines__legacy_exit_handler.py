from kfp import pipeline
from kfp.dsl import component
from google.cloud import storage


@component
def legacy_exit_handler(url: str) -> None:
    """Legacy function to handle exit gracefully."""
    print(f"Downloading from {url}...")
    # Simulate a download operation
    # For demonstration, we'll just print a message
    print("Download completed.")


@pipeline(name="Exit Handler")
def exit_handler_pipeline():
    """Pipeline to demonstrate the Exit Handler component."""
    legacy_exit_handler("gs://example-bucket/data.txt")


# Run the pipeline
exit_handler_pipeline()
