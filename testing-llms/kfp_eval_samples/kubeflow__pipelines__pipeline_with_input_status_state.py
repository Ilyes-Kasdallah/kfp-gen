```python
import kfp
from kfp import dsl

# Define the echo_state component
@dsl.component(
    base_image='ubuntu',
    outputs=['output']
)
def echo_state(final_status: dsl.PipelineTaskFinalStatus):
    assert final_status.state == 'COMPLETE'
    assert final_status.job.resource_name.endswith('status-state-pipeline')
    assert final_status.task.name == 'exit-handler-1'

# Define the some_task component
@dsl.component(
    base_image='ubuntu'
)
def some_task():
    print("Executing some_task()...")

# Define the pipeline
@dsl.pipeline(name="status_state_pipeline")
def status_state_pipeline():
    # Execute some_task within an ExitHandler
    exit_handler = dsl.ExitHandler(
        exit_task=echo_state,
        on_failure=True,
        on_success=False
    )
    
    # Execute some_task
    some_task()

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(status_state_pipeline)

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment('My Experiment')
run = client.run(experiment.id, pipeline_func=compiled_pipeline)
```

This code snippet defines a Kubeflow Pipeline named `status_state_pipeline` that includes two components: `echo_state` and `some_task`. The `echo_state` component validates the status of a previous pipeline task, ensuring it meets specific criteria before proceeding. The `some_task` component simply prints a message to the console. The pipeline structure uses an `ExitHandler` to ensure `echo_state` is always executed, even if `some_task` fails. The pipeline is compiled and submitted to a Kubeflow cluster using the Kubeflow Pipelines SDK.