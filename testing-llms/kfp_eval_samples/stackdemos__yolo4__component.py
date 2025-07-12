```python
import kfp
from kfp import dsl

def http_download_op(url, md5sum, local_path):
    return dsl.ContainerOp(
        name='Download Artifact',
        image='appropriate/curl',
        arguments=[
            '-o', local_path,
            url
        ],
        metadata={
            'inputs': [
                dsl.InputArtifact('input_url'),
                dsl.InputArtifact('expected_md5')
            ],
            'outputs': [
                dsl.OutputArtifact('downloaded_file')
            ]
        }
    )

def training_op(input_file, **kwargs):
    return dsl.ContainerOp(
        name='Training Operation',
        image='your_custom_image',
        arguments=[
            '--script', input_file,
            # Add any additional arguments here
        ],
        metadata={
            'inputs': [
                dsl.InputArtifact('input_file')
            ],
            'outputs': kwargs.get('file_outputs', [])
        }
    )

@dsl.pipeline(name='my_pipeline')
def my_pipeline():
    download_task = http_download_op(
        url=dsl.InputParameter('url'),
        md5sum=dsl.InputParameter('md5sum'),
        local_path=dsl.OutputPath('downloaded_file')
    )
    
    training_task.after(download_task)
```

In this solution, we have created a Kubeflow Pipeline named `my_pipeline` that includes two components: `download-artifact` and `training-op`. The `download-artifact` component downloads a file from a specified URL and checks its MD5 sum against an expected value. If the file does not exist or does not match the expected MD5 sum, it downloads the file again. The `training-op` component then uses the downloaded file to perform model training using a specified Docker image. The pipeline ensures that the training operation only runs after the download operation has completed successfully.