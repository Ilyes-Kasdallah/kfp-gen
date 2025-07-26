from kfp import components
from kfp.dsl import pipeline, Input, Output

# Import necessary libraries
from kfp.dsl._transformers import ContainerOpTransform


@pipeline(name="_transformers_test")
def KubeflowContainerOpTransformPipeline(
    container_op: Input[ContainerOp],
    # Add more parameters as needed
):
    # Apply transformations to the container_op
    transformed_container_op = ContainerOpTransform(container_op)

    # Return the transformed container_op
    return transformed_container_op
