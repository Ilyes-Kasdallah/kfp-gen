import kfp
import kfp.dsl as dsl
from kfp.components import func_to_container_op

@func_to_container_op
def show_results(linear_regression : float) -> None:

    print(f"Linear regression (accuracy): {linear_regression}")

@dsl.pipeline(name='Boston Housing Pipeline', description='Test kubeflow pipline for Boston Housing dataset .')
def first_pipeline():

    download = kfp.components.load_component_from_file('download_data/download_data.yaml')
    linear_regression = kfp.components.load_component_from_file('linear_regression/linear_regression.yaml')

    download_task = download()

    linear_regression_task = linear_regression(download_task.output)

    show_results(linear_regression_task.output)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(first_pipeline, 'LinearPipline.yaml')
