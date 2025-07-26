
from kfp import pipeline
from kfp.components import download_artifact

@pipeline(name="my-data-processing-pipeline")
def my_data_processing_pipeline():
    # Download artifact from URL
    download_artifact(
        name="downloaded_file",
        url="https://example.com/data.csv",
        destination="/path/to/downloaded_file"
    )
