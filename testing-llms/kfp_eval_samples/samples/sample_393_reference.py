import kfp
from kfp import dsl


def preprocess_op():
    return dsl.ContainerOp(
        name='Preprocess Data',
        image='shanau2/tf_pipeline_preprocess:v0.2',
        arguments=[
        ],
        file_outputs={
            'x_train': '/tmp/data/x_train.pickle',
            'x_test': '/tmp/data/x_test.pickle',
            'y_train': '/tmp/data/y_train.pickle',
            'y_test': '/tmp/data/y_test.pickle',
            'model_dir': 'tmp/data'
        }
    )


def train_op(x_train, y_train, model_dir):
    return dsl.ContainerOp(
        name='Train Model',
        image='shanau2/tf_pipeline_train:v0.1',
        arguments=[
            '--x-train', x_train,
            '--y_train', y_train,
            '--model_dir', model_dir
        ],
        file_outputs={
            'model_dir': model_dir,
        }
    )


# def test_op(x_test, y_test, model_dir, output_dir):
#     return dsl.ContainerOp(
#         name='Test Model',
#         image='shanau2/boston_pipeline_test:v3',
#         arguments=[
#             '--x_test', x_test,
#             '--y_test', y_test,
#             '--model_dir', model_dir,
#             '--output-dir', output_dir,
#         ],
#         file_outputs={
#             'output_dir': output_dir,
#         }
#     )


# def deploy(output_dir):
#     return dsl.ContainerOp(
#         name='Deploy Model',
#         image='shanau2/tf_pipeline_deploy_model:v0.1',
#         arguments=[
#             '--output_dir', output_dir
#         ]
#     )


@dsl.pipeline(
    name='Fashion MNIST Training Pipeline',
    description='Fashion MNIST Training Pipeline to be executed on KubeFlow.'
)
def training_pipeline():
    _preprocess_op = preprocess_op()

    _train_op = train_op(
        dsl.InputArgumentPath(_preprocess_op.outputs['x_train']),
        dsl.InputArgumentPath(_preprocess_op.outputs['y_train']),
        dsl.InputArgumentPath(_preprocess_op.outputs['model_dir']),
    ).after(_preprocess_op)

    # _test_op = test_op(
    #     dsl.InputArgumentPath(_preprocess_op.outputs['x_test']),
    #     dsl.InputArgumentPath(_preprocess_op.outputs['y_test']),
    #     dsl.InputArgumentPath(_train_op.outputs['model_dir'])
    # ).after(_train_op)

    # deploy_model_op(
    #     dsl.InputArgumentPath(_train_op.outputs['model_dir'])
    # ).after(_test_op)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(training_pipeline, 'demo.tar.gz')

