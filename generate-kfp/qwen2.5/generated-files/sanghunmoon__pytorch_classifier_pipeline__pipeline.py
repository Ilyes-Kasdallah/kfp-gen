
from kfp import dsl

@dsl.pipeline(name="pytorch_classifier_test_2")
def pytorch_classifier_test_2():
    # Define the training pipeline component
    training_pipeline = dsl.ContainerOp(
        name="training_pipeline",
        image="lego0142/pytorch_classifier:1.1",
        command=["python", "train.py"],
        args=["--data_dir=/path/to/data"]
    )
    
    # Return the training pipeline component
    return training_pipeline
