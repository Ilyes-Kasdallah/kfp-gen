
from kfp import dsl

@dsl.pipeline(name="my_pipeline")
def my_pipeline(
    url: str,
    download_to: str,
    md5sum: str,
):
    # Download the data artifact
    download_artifact(
        url=url,
        download_to=download_to,
        md5sum=md5sum,
    )
