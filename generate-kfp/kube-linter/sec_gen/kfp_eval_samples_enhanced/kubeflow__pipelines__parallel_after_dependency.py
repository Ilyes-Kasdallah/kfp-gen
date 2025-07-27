import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="loop_with_after_dependency_set")
def loop_with_after_dependency_set():
    # Define the first component
    @component(name="print_op")
    def print_op(message):
        print(message)
        return message

    # Define the second component
    @component(name="print_op2")
    def print_op2(message):
        print(message)
        return message

    # Define the third component
    @component(name="print_op3")
    def print_op3(message):
        print(message)
        return message

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Define the dependencies between components
    # Dependency 1: print_op -> print_op2
    print_op2.depends_on(print_op)

    # Dependency 2: print_op2 -> print_op3
    print_op3.depends_on(print_op2)

    # Execute the pipeline
    print("Executing pipeline...")
    kfp.compiler.Compiler().compile(pipeline_root)
