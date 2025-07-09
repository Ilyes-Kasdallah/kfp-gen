
from kfp import dsl
from kfp import compiler
import os


@dsl.pipeline(name='My Pipeline', description='A pipeline with 3 steps')
def my_pipeline():
    data_prep = dsl.ContainerOp(
        name='Data Preparation',
        image='quynhtl/today_code1:latest',
        command=['python', 'download.py'],
        file_outputs = {"output": "/data"}
    )

    model_train = dsl.ContainerOp(
        name='Model Training',
        image='quynhtl/today_code1:latest',
        command=['python', 'model_train.py'],
        arguments=['--input-folder', data_prep.output]
    )
    model_train.after(data_prep)

    # model_version = dsl.ContainerOp(
    #     name='Model Versioning',
    #     image='quynhtl/today_code1:latest',
    #     command=['python', 'version_data.py'],
    #     arguments=['--model-dir', model_train.outputs['model_path'], '--version-dir', '/version']
    # )
    # model_version.after(model_train)


if __name__ == '__main__':
    compiler.Compiler().compile(my_pipeline, 'my_pipeline.zip')