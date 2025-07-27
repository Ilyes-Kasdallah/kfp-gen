import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the _transformers function as a Kubeflow step
@component
def _transformers(container_ops):
    # Apply transformations to all ContainerOps in the pipeline
    for op in container_ops:
        # Example transformation: convert image to PDF
        op.transform_image_to_pdf()
        # Example transformation: add metadata to the image
        op.add_metadata_to_image("description", "This is a sample image")
    return container_ops


# Define the pipeline function
@pipeline(name="_transformers_pipeline")
def demo():
    # Get the pipeline configuration
    pipeline_conf = kfp.dsl.get_pipeline_conf()

    # Add the _transformers function to the pipeline
    pipeline_conf.add_op_transformer(_transformers)

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Compile the pipeline
    pipeline = pipeline_conf.compile(pipeline_root=pipeline_root)

    return pipeline


# Example usage of the demo pipeline
if __name__ == "__main__":
    demo()
