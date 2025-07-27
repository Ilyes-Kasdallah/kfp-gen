import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the nvidia_smi component
@component
def nvidia_smi():
    # Execute the nvidia-smi command
    result = kfp.components.execute_command(
        command="nvidia-smi",
        image="quay.io/modh/cuda-notebooks:cuda-jupyter-minimal-ubi9-python-3.11-20250326",
    )
    return result


# Define the pipeline function
@pipeline(name="12_gpu_task_pipeline")
def one_gpu_task_pipeline():
    # Call the nvidia_smi component
    gpu_info = nvidia_smi()

    # Output the GPU information
    Output("gpu_info", gpu_info)


# Compile the pipeline
kfp.compiler.Compiler().compile(one_gpu_task_pipeline)
