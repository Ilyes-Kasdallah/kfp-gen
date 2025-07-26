
from kubeflow.pipelines import pipeline, component

@dsl.pipeline(name="resnet_cifar10")
def resnet_cifar10(input_dir, output_dir):
    # PreprocessOp component
    preprocess_op = component(
        name="preprocess",
        image="muneer7589/k_pipeline_preprocess:latest",
        inputs=[
            "input_dir",
        ],
        outputs=[
            "output.txt",
        ],
    )

    # DeployOp component
    deploy_op = component(
        name="deploy",
        image="muneer7589/k_pipeline_deploy:latest",
        inputs=[
            "output_dir",
        ],
        outputs=[
            "model.tar.gz",
        ],
    )

    # Combine the components into a single pipeline
    return pipeline(
        steps=[
            preprocess_op,
            deploy_op,
        ],
    )
