```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='taxi-on-prem')
def taxi_on_prem(
    inference_data: dsl.InputArtifact,
    validation_data: dsl.InputArtifact,
    column_names: dsl.InputParameter,
    key_columns: dsl.InputParameter,
    project: dsl.InputParameter,
    mode: dsl.InputParameter,
    train_data: dsl.InputArtifact,
    evaluation_data: dsl.InputArtifact,
    schema: dsl.OutputArtifact,
    transform_output: dsl.OutputArtifact,
    training_output: dsl.OutputArtifact,
    learning_rate: dsl.InputParameter,
    hidden_layer_size: dsl.InputParameter,
    steps: dsl.InputParameter,
    target: dsl.InputParameter,
    preprocess_module: dsl.InputParameter
):
    # Dataflow TF Data Validation Op
    dataflow_tf_data_validation = dsl.ContainerOp(
        name='dataflow_tf_data_validation',
        image='gcr.io/ml-pipeline/ml-pipeline-dataflow-tfdv:6ad2601ec7d04e842c212c50d5c78e548e12ddea',
        arguments=[
            '--input-data', inference_data.path,
            '--validation-data', validation_data.path,
            '--column-names', column_names,
            '--key-columns', key_columns,
            '--project', project,
            '--mode', mode
        ],
        outputs={
            '/schema.txt': schema,
            '/output_validation_result.txt': dsl.OutputArtifact(type=dsl.ArtifactType.TEXT)
        },
        mount_paths={
            '/volume': transform_output.path
        }
    )

    # Dataflow TF Transform Op
    dataflow_tf_transform = dsl.ContainerOp(
        name='dataflow_tf_transform',
        image='gcr.io/ml-pipeline/ml-pipeline-dataflow-tft:6ad2601ec7d04e842c212c50d5c78e548e12ddea',
        arguments=[
            '--train-data', train_data.path,
            '--evaluation-data', evaluation_data.path,
            '--schema', schema.path,
            '--project', project,
            '--preprocess-mode', preprocess_mode,
            '--preprocess-module', preprocess_module
        ],
        outputs={
            '/output.txt': transform_output
        },
        mount_paths={
            '/volume': training_output.path
        }
    )

    # TF Train Op
    tf_train = dsl.ContainerOp(
        name='tf_train',
        image='gcr.io/ml-pipeline/ml-pipeline-kubeflow-tf-trainer:5df2cdc1ed145320204e8bc73b59cdbd7b3da28f',
        arguments=[
            '--transformed-data-dir', transform_output.path,
            '--schema', schema.path,
            '--learning-rate', learning_rate,
            '--hidden-layer-size', hidden_layer_size,
            '--steps', steps,
            '--target', target,
            '--preprocess-module', preprocess_module
        ],
        outputs={
            '/trained-model': training_output
        },
        mount_paths={
            '/volume': training_output.path
        }
    )
```

This code defines a Kubeflow Pipeline named `taxi-on-prem` with three components: `dataflow_tf_data_validation_op`, `dataflow_tf_transform_op`, and `tf_train_op`. Each component is defined using the `dsl.ContainerOp` class, which specifies the container image, command-line arguments, outputs, and mount paths. The pipeline uses persistent volumes for data storage and transfer between components.