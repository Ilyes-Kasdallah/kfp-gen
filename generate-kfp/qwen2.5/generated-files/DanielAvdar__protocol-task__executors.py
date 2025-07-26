
from kfp import dsl

@dsl.pipeline(name="ArtifactProcessingPipeline")
def ArtifactProcessingPipeline(task_params, task_module):
    # Initialize the task
    artifacttaskinitexecutor(
        task_params=task_params,
        task_module=task_module,
        output_artifact="processed_output"
    )
