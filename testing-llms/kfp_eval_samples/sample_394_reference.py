import kfp
from kfp import dsl


def demo_op():
    return dsl.ContainerOp(name='demo', image='demo:v0.0.1')


@dsl.pipeline(
    name='demo',
    description='test'
)
def pipeline():
    op = demo_op()


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.zip')
