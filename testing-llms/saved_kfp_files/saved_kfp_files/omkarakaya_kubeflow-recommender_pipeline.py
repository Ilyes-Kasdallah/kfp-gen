import kfp.dsl as dsl
import kfp.gcp as gcp
import kfp.onprem as onprem

from string import Template
import json

@dsl.pipeline(
  name='Kubeflow Pipeline Test',
  description='Kubeflow Pipeline Test'
)
def xgb_train_pipeline(
    output,
    project,
    region='us-central1',
    train_data='gs://ml-pipeline-playground/sfpd/train.csv',
    eval_data='gs://ml-pipeline-playground/sfpd/eval.csv',
    schema='gs://ml-pipeline-playground/sfpd/schema.json',
    target='resolution',
    rounds=200,
    workers=2,
    true_label='ACTION'):
    #vol_common = dsl.PipelineVolume()
    vol_common = dsl.VolumeOp(
        name="create_pvc",
        resource_name="my-pvc",
        modes=dsl.VOLUME_MODE_RWO,
        size="1Gi"
    )

    preprocess = dsl.ContainerOp(
        name='preprocess',
        image='gcr.io/compose-flask/hub:v6',
        arguments=[
            '--project', project,
            '--mode', 'cloud',
        ],
        file_outputs={'output': '/tmp/output.txt'},
        pvolumes={"/data": vol_common.volume}
    )
    preprocess.after(vol_common)
    build = dsl.ContainerOp(
        name='build',
        image='gcr.io/compose-flask/build:v6',
        arguments=[
            '--project', project,
            '--mode', 'cloud',
            '--preprocessed', preprocess.outputs['output'],
            '--preprocessed2', preprocess.output
        ],
        file_outputs={'output': '/tmp/output.txt'},
        pvolumes={"/data": vol_common.volume}
    )
    build.after(vol_common)
    build.after(preprocess)