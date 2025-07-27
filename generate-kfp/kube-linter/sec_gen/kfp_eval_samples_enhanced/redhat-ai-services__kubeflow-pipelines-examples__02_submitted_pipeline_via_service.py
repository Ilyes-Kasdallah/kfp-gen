import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="add_pipeline")
def add_pipeline(a: float, b: float):
    # Define the add component
    @dsl.component(name="add")
    def add(a: float, b: float) -> float:
        return a + b

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Define the pipeline steps
    add_task = add(a, b)
    add_task.output("sum", type=Output[Dataset])

    # Define the pipeline execution
    pipeline.add_steps([add_task])

    # Compile the pipeline
    kfp.compiler.Compiler().compile(add_pipeline, pipeline_root)
