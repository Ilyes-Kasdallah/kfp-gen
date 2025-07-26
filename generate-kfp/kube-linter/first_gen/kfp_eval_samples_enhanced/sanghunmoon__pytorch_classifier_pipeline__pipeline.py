import kfp
from kfp.dsl import ContainerOp, Output, Pipeline

# Define the pipeline function name
pipeline_name = "pytorch_classifier_test_2"


# Define the training pipeline component
@dsl.pipeline(name=pipeline_name)
def training_pipeline():
    # Define the Docker container
    container_op = ContainerOp(
        name="training_container",
        image="lego0142/pytorch_classifier:1.1",
        command=["python", "train.py"],
        args=["data_path=/path/to/data"],
    )

    # Define the output artifact
    output_artifact = Output(type=kfp.types.Blob)

    # Return the output artifact
    return output_artifact


# Run the pipeline
if __name__ == "__main__":
    pipeline = training_pipeline()
    pipeline.run()
