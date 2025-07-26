from kfp import components
from kfp.dsl import pipeline


@dsl.pipeline(name="pipeline-with-placeholders")
def pipeline_with_placeholders():
    # Define the print_all_placeholders component
    @components.component
    def print_all_placeholders(job_name, task_name):
        print(f"Job Name: {job_name}, Task Name: {task_name}")

    # Execute the print_all_placeholders component
    print_all_placeholders("my-pipeline-job", "my-task")


# Run the pipeline
pipeline_with_placeholders()
