import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="pipeline-with-placeholders")
def pipeline_with_placeholders():
    # Define the single component
    @component
    def print_all_placeholders(job_name, task_info):
        # Print the placeholders
        print(f"Job Name: {job_name}")
        print(f"Task Info: {task_info}")


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(pipeline_with_placeholders)

# Output the compiled pipeline
print(compiled_pipeline)
