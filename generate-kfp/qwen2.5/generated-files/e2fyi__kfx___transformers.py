
from kfp import dsl

@dsl.pipeline(name='demo')
def demo():
    # Define a simple transformation function
    def _transformers(container_op):
        # Example transformation: add a label to the container
        container_op.add_label('transformed')

    # Apply the transformation to all ContainerOps in the pipeline
    for container_op in dsl.get_pipeline_conf().get_all_op_names():
        _transformers(container_op)

# Run the pipeline
demo()
