
from kfp import pipeline
from kfp.components import download

@dsl.pipeline(name="First Pipeline")
def first_pipeline():
    # Download the necessary data
    download(download_data.download_data.yaml)
