import kfp
from kfp import dsl

def mount_emptydir(name=None, mount_path='/tmp'):
  from kubernetes import client as k8sc
  if not name:
    import uuid
    name=str(uuid.uuid4())[:8]
  
  def _mount_emptydir(task):
    task.add_volume(
      k8sc.V1Volume(
        name=name,
        empty_dir=k8sc.V1EmptyDirVolumeSource()
      )
    )
    task.add_volume_mount(
      k8sc.V1VolumeMount(
        name=name,
        mount_path=mount_path
      )
    )
    return task
  
  return _mount_emptydir

def preprocess_op():
    return dsl.ContainerOp(
        name='Preprocess Data',
        image='kang/preprocess:v30'
    )


def train_op():
    return dsl.ContainerOp(
        name='Train Model',
        image='kang/train:v30'
    )


def test_op():
    return dsl.ContainerOp(
        name='Test Model',
        image='kang/test:v30'
    )

def serve_op():
    return dsl.ContainerOp(
        name='Serve Model',
        image='kang/serve:v10'
    )


@dsl.pipeline(
    name='Translation Pipeline',
    description='An example pipeline that translate from Chinese to English.'
)

def translation_pipeline():
    _preprocess_op = preprocess_op()
    _preprocess_op.apply(mount_emptydir(mount_path='/tmp'))

    _train_op = train_op().after(_preprocess_op)
    _train_op.apply(mount_emptydir(mount_path='/tmp'))

    _test_op = test_op().after(_train_op)
    _test_op.apply(mount_emptydir(mount_path='/tmp'))

    _serve_op = serve_op().after(_test_op)
    _serve_op.apply(mount_emptydir(mount_path='/tmp')) 

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(translation_pipeline, __file__ + '.yaml')
