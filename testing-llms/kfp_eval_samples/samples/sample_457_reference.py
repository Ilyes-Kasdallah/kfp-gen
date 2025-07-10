import kfp
from kfp import dsl
from app.preprocess_data.kf_preprocess_component import preprocess_op
from app.train.kf_train_component import train_op
from app.test.kf_test_component import test_op
from app.deploy.kf_deploy_component import deploy_model_op

@dsl.pipeline(
    name='Boston Housing Pipeline',
    description='An example pipeline.'
)
def boston_pipeline():
    _preprocess_op = preprocess_op()

    _train_op = train_op(
        dsl.InputArgumentPath(_preprocess_op.outputs['x_train']),
        dsl.InputArgumentPath(_preprocess_op.outputs['y_train'])
    ).after(_preprocess_op)

    _test_op = test_op(
        dsl.InputArgumentPath(_preprocess_op.outputs['x_test']),
        dsl.InputArgumentPath(_preprocess_op.outputs['y_test']),
        dsl.InputArgumentPath(_train_op.outputs['model'])
    ).after(_train_op)

    deploy_model_op(
        dsl.InputArgumentPath(_train_op.outputs['model'])
    ).after(_test_op)



host='http://kf-centraldashboard.k8sdev.infolytx.tech/pipeline/'
namespace='sazzad'


client = kfp.Client(host=host, namespace=namespace)
client.create_run_from_pipeline_func(boston_pipeline, arguments={}, experiment_name= "Boston Housing Pipeline Experiment")
