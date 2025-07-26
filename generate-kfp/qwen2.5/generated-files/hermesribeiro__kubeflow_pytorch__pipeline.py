
from kfp import dsl

@dsl.pipeline(name="CIFAR Pytorch")
def cifar_pytorch():
    # Define the model train component
    train_component = dsl.component(
        name="train",
        image="hermesribeiro/cifar:latest",
        command=["python", "train.py"],
        args=["--data_dir", "/path/to/cifar/data"]
    )

    # Define the model evaluation component
    eval_component = dsl.component(
        name="eval",
        image="hermesribeiro/cifar:latest",
        command=["python", "evaluate.py"],
        args=["--data_dir", "/path/to/cifar/data"]
    )

    # Define the pipeline
    return dsl.Pipeline(
        name="CIFAR Pytorch Pipeline",
        steps=[
            train_component,
            eval_component
        ]
    )
