
from kfp import pipeline
from kfp.components import download

@dsl.pipeline(name="First Pipeline")
def first_pipeline():
    # Download the dataset
    download(download_data.download_data.yaml)
