
from kfp import dsl

@dsl.pipeline(name="my_pipeline")
def my_pipeline(url: str, download_to: str):
    # Download the file from the given URL
    download_artifact(
        url=url,
        download_to=download_to,
        name="download_artifact"
    )
