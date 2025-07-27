import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="A Simple CI Pipeline")
def A_Simple_CI_Pipeline():
    # Define the first component: add_op
    @dsl.component(name="add_op")
    def add_op(x_value, y_value):
        return x_value + y_value

    # Define the second component: add_op
    @dsl.component(name="add_op")
    def add_op(x_value, y_value):
        return x_value + y_value

    # Define the third component: add_op
    @dsl.component(name="add_op")
    def add_op(x_value, y_value):
        return x_value + y_value


# Define the pipeline root
pipeline_root = "gs://my-bucket/pipeline-root"

# Compile the pipeline
kfp.compiler.Compiler().compile(A_Simple_CI_Pipeline, pipeline_root)
