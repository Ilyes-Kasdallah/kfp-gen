import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from kfp.components import train_model, evaluate_model

# Define the pipeline function name
pipeline_name = "CIFAR Pytorch"


# Define the pipeline
@pipeline(name=pipeline_name)
def cifar_pytorch():
    # Define the model train component
    train_component = train_model(
        image="hermesribeiro/cifar:latest",
        train_script="train.py",
        model_dir="/path/to/model/directory",
    )

    # Define the model evaluation component
    evaluate_component = evaluate_model(
        image="hermesribeiro/cifar:latest", model_dir="/path/to/model/directory"
    )

    # Return the pipeline
    return train_component, evaluate_component


# Example usage of the pipeline
if __name__ == "__main__":
    pipeline(cifar_pytorch())
