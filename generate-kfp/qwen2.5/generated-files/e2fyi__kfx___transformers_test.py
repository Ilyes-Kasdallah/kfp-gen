
from kfp import dsl
from kfp.components import _transformers

@dsl.pipeline(name="KubeflowContainerOpTransformPipeline")
def KubeflowContainerOpTransformPipeline():
    # Define the input ContainerOp
    container_op = dsl.ContainerOp(
        name="input_container_op",
        image="gcr.io/kubeflow/pipelines:latest",
        command=["echo", "Hello, Kubeflow!"],
        env_vars={"MY_VAR": "value"},
    )

    # Define the transformation component
    transform_component = _transformers.ContainerOpTransform(
        name="transform_component",
        container_op=container_op,
        transformers=[
            _transformers.Transform("echo", "echo"),
            _transformers.Transform("env_vars", "setenv MY_VAR=value"),
        ],
    )

    # Define the output ContainerOp after transformation
    output_container_op = transform_component.apply(container_op)

    return output_container_op
