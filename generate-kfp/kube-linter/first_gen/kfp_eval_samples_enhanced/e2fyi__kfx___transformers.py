import kfp
from kfp.dsl import pipeline, component


@pipeline(name="_transformers")
def demo():
    # Define a function to transform a ContainerOp
    @component
    def transform_container_op(container_op):
        # Example transformation logic
        transformed_container_op = container_op.copy()
        transformed_container_op.name = f"Transformed_{container_op.name}"
        return transformed_container_op

    # Apply the transformation to all ContainerOps in the pipeline
    for container_op in kfp.dsl.get_pipeline_conf().get_all_op_names():
        transformed_container_op = transform_container_op(container_op)
        print(f"Transformed {container_op}: {transformed_container_op}")


# Run the pipeline
demo()
