```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from files
optuna_worker = load_component_from_file('optuna-worker.yaml')
slack_notification = load_component_from_file('slack-notification.yaml')

# Define the pipeline
@dsl.pipeline(name='optuna pipeline')
def optuna_pipeline(
    pipeline_name: str,
    bucket_name: str,
    job_id: str,
    n_trials: int,
    n_jobs: int,
    training_pipeline_name: str,
    dataset: str,
    epochs: int
):
    # Execute the optuna worker component
    optuna_worker(pipeline_name=pipeline_name,
                  bucket_name=bucket_name,
                  job_id=job_id,
                  n_trials=n_trials,
                  n_jobs=n_jobs,
                  training_pipeline_name=training_pipeline_name,
                  dataset=dataset,
                  epochs=epochs)

    # Define an exit handler to send a slack notification
    @dsl.exit_handler
    def on_exit():
        slack_notification(pipeline_name=pipeline_name,
                          job_id=job_id,
                          message=f'Pipeline {pipeline_name} completed.')

# Compile the pipeline into a YAML file
kfp.compiler.Compiler().compile(optuna_pipeline, 'optuna-pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `optuna pipeline` that performs hyperparameter optimization using Optuna. It includes the necessary components (`optuna-worker` and `slack-notification`) and their respective configurations. The pipeline's control flow ensures that the `slack-notification` component runs after the `optuna-worker` component, regardless of its outcome. The pipeline is compiled into a YAML file for deployment.