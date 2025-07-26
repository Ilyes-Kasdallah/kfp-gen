from kfp import components
from kfp.dsl import pipeline


# Define the ArtifactProcessingPipeline
@pipeline(name="ArtifactProcessingPipeline")
def ArtifactProcessingPipeline(task_params: dict, task_module: str) -> None:
    # Initialize the task
    artifacttaskinitexecutor(
        task_params=task_params,
        task_module=task_module,
        output_artifact="processed_output",
    )
