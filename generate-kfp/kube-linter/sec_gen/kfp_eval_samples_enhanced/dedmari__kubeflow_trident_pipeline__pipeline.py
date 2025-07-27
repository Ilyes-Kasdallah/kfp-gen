import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="resnet_cifar10")
def resnet_cifar10(
    input_dir: Input[Dataset],
    output_dir: Output[Dataset],
    model_dir: Output[Model],
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Preprocess the input dataset
    preprocess_op = component(
        name="preprocess_op",
        inputs={"input_dir": input_dir},
        outputs={"output_dir": output_dir},
        code="kfp.components.preprocess.preprocess",
        parameters={
            "cache": cache,
            "retries": retries,
            "resource_limits": resource_limits,
        },
    )

    # Deploy the model
    deploy_model_op = component(
        name="deploy_model_op",
        inputs={"model_dir": model_dir},
        outputs={"output_dir": output_dir},
        code="kfp.components.deploy.deploy",
        parameters={
            "cache": cache,
            "retries": retries,
            "resource_limits": resource_limits,
        },
    )

    # Return the output directories
    return preprocess_op.output_dir, deploy_model_op.output_dir
