import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="my_pipeline")
def my_pipeline(
    url: str,
    download_to: Output[Dataset],
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Download the artifact from the URL
    download_artifact(
        url=url,
        download_to=download_to,
        cache=cache,
        retries=retries,
        resource_limits=resource_limits,
    )
