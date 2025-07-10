import kfp
from kfp import dsl

@dsl.pipeline(
    name='Simple Pipeline',
    description='A simple pipeline for testing kfp'
)
def simple_pipeline():
    op = dsl.ContainerSpec(
        image='busybox',
        command=['echo', 'Hello from Kubeflow Pipelines!']
    )

# Compile the pipeline to a YAML file
kfp.compiler.Compiler().compile(simple_pipeline, 'simple_pipeline.yaml')

print("Pipeline compiled successfully!")
