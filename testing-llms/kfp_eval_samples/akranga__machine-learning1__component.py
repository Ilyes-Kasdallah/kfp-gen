```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='my-pipeline')
def my_pipeline(url: str, download_to: str, md5sum: str,
                script: str = 'preprocess_data.py',
                training_image: str = None):
    # Download the artifact
    download_artifact = dsl.ContainerOp(
        name='download-artifact',
        image='appropriate/curl',
        arguments=[
            '-L', url,
            '-o', download_to,
            '--insecure'
        ],
        metadata={
            'inputs': [
                dsl.InputArtifact('url'),
                dsl.OutputArtifact('downloaded_file')
            ],
            'outputs': [
                dsl.OutputArtifact('md5sum')
            ]
        }
    )

    # Preprocess the data
    preprocess_data = dsl.ContainerOp(
        name='preprocess-data',
        image=training_image if training_image else 'your-container-image',
        arguments=[
            '-f', download_artifact.outputs['downloaded_file'].path,
            '-s', script
        ],
        metadata={
            'inputs': [
                dsl.InputArtifact('downloaded_file')
            ],
            'outputs': [
                dsl.OutputArtifact('preprocessed_data')
            ]
        }
    )

    # Train the model
    train_model = dsl.ContainerOp(
        name='train-model',
        image=training_image if training_image else 'your-container-image',
        arguments=[
            '-p', preprocess_data.outputs['preprocessed_data'].path,
            '-s', script
        ],
        metadata={
            'inputs': [
                dsl.InputArtifact('preprocessed_data')
            ],
            'outputs': [
                dsl.OutputArtifact('trained_model')
            ]
        }
    )
```

This code defines a Kubeflow Pipeline named `my-pipeline` with three components: `download-artifact`, `preprocess-data`, and `train-model`. Each component is defined using the `dsl.ContainerOp` class, which represents a step in the pipeline. The pipeline's control flow is sequential, with each component running after the previous one. The `training_op` and `http_download_op` custom functions are assumed to be defined elsewhere in the codebase.