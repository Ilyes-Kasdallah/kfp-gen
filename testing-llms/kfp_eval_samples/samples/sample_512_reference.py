from kfp import dsl

def write():
    return dsl.ContainerOp(
        name='Write',
        image='busybox',
        command=['sh', '-c'],
        arguments=['echo "Hello" > /mnt/data/kubeflow/hello_world.txt'],
        pvolumes={'/mnt/data/kubeflow': dsl.PipelineVolume(pvc='my-pvc')}
    )

def read():
    return dsl.ContainerOp(
        name='Read',
        image='busybox',
        command=['sh', '-c'],
        arguments=['cat /mnt/data/kubeflow/hello_world.txt'],
        pvolumes={'/mnt/data/kubeflow': dsl.PipelineVolume(pvc='my-pvc')}
    )

@dsl.pipeline(
    name='Hello World',
    description='A pipeline to demonstrate use of PersistentVolumeClaim'
)
def pvc_pipeline():
    producer = write()
    consumer = read().after(producer)

if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(pvc_pipeline, 'hello_world.yaml')
