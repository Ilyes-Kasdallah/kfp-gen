```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load the preprocessing component from the specified Docker image
preprocessing = load_component_from_file('pharmbio/pipelines-kensert-preprocess:test')

# Define the pipeline
@dsl.pipeline(name='Kensert_CNN_test')
def Kensert_CNN_pipeline(
    model_type='Inception_v3',
    checkpoint_preprocess='false',
    workspace_name='kensert_CNN',
    artifact_bucket=None,
    checkpoint_training=None,
    checkpoint_evaluation=None,
    model_repo=None
):
    # Execute the preprocessing component
    preprocessing_op = preprocessing(
        model_type=model_type,
        checkpoint_preprocess=checkpoint_preprocess,
        workspace_name=workspace_name,
        artifact_bucket=artifact_bucket,
        checkpoint_training=checkpoint_training,
        checkpoint_evaluation=checkpoint_evaluation,
        model_repo=model_repo
    )

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(pipeline)

# Submit the compiled pipeline to the Kubeflow Pipelines server
kfp.Client().create_run_from_pipeline_func(compiled_pipeline)
```

This code defines a Kubeflow Pipeline named `Kensert_CNN_test` that includes a single component: `preprocessing`. The pipeline is executed using the `kfp` library, which handles the orchestration of the pipeline's steps. The `preprocessing` component is loaded from a Docker image and configured with various parameters such as `model_type`, `checkpoint_preprocess`, and `workspace_name`. The pipeline is then compiled and submitted to the Kubeflow Pipelines server for execution.