from kfp import dsl
from kfp.dsl import Input, Dataset


@dsl.component(base_image="python:3.10")
def read_dataset(dataset: Input[Dataset]):
    with open(dataset.path, "r") as f:
        data = f.read()
    print("Dataset content:", data)


@dsl.pipeline
def pipeline():
    importer_task = dsl.importer(
        artifact_uri="minio://mlpipeline/artifacts/input/raw_transaction_datasource.csv",
        artifact_class=dsl.Dataset,
        reimport=True)

    read_dataset(dataset=importer_task.output)
