from kfp import components, dsl, compiler, Client

from components.fetch_data import fetch_data, split_data
from components.model import train
from utils.git import create_version_name

BASE_IMAGE = 'dabarnyarddawg/kf-pipelines-base-images:latest'
CLIENT = 'http://127.0.0.1:8080'
PIPELINE_NAME = 'cancer-classifier'
EXPERIMENT_NAME = 'cancer_detection'

fetch_data_op = components.create_component_from_func(fetch_data, base_image=BASE_IMAGE)
split_data_op = components.create_component_from_func(split_data, base_image=BASE_IMAGE)
train_op = components.create_component_from_func(train, base_image=BASE_IMAGE)


@dsl.pipeline(name=PIPELINE_NAME, description='test classifier pipeline with breast cancer dataset')
def pipeline(test_size: float = 0.2):
    fetch_data_task = fetch_data_op()
    split_data_task = split_data_op(x=fetch_data_task.outputs['x'], y=fetch_data_task.outputs['y'], test_size=test_size)
    # TODO: train model(s) (with tuning) in parallel?
    train_task = train_op(x=split_data_task.outputs['x_train'], y=split_data_task.outputs['y_train'])
    # TODO: batch predictions (move to separate pipeline)
    # TODO: serve model


if __name__ == '__main__':
    client = Client(host=CLIENT)
    client.create_run_from_pipeline_func(
        pipeline, arguments={}, run_name=create_version_name(), experiment_name=f'{EXPERIMENT_NAME}_dev'
    )
    # TODO: github action to compile & deploy pipeline on release
    # TODO: unit tests on commit
    # TODO: connect artifacts to local storage mount
