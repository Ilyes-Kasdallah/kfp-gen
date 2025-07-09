from kfp.dsl import component
from typing import NamedTuple

@component(
    packages_to_install=['kserve', 'boto3'],
)
def deploy_model_with_kserve_sdk(
    model_name: str,
    model_bucket: str,
    model_key: str,
    minio_endpoint: str = 'minio:9000',
    minio_access_key: str = 'minio',
    minio_secret_key: str = 'minio123',
    namespace: str = 'kubeflow'
) -> NamedTuple('Outputs', [
    ('inference_service_name', str),
    ('status', str),
]):
    from kserve import KServeClient, constants
    from kserve.models import (
        V1beta1InferenceService,
        V1beta1InferenceServiceSpec,
        V1beta1PredictorSpec,
        V1beta1SKLearnSpec,
        V1beta1ModelSpec,
    )
    import boto3
    from collections import namedtuple

    # Validate the model exists in MinIO
    s3 = boto3.client(
        's3',
        endpoint_url=f'http://{minio_endpoint}',
        aws_access_key_id=minio_access_key,
        aws_secret_access_key=minio_secret_key,
        config=boto3.session.Config(signature_version='s3v4'),
        verify=False
    )

    try:
        s3.head_object(Bucket=model_bucket, Key=model_key)
        print(f"Model '{model_key}' found in bucket '{model_bucket}'.")
    except Exception as e:
        raise RuntimeError(f"Model not found: {e}")

    # Initialize the KServe client
    kserve_client = KServeClient()

    # Create the InferenceService spec using the KServe SDK
    inference_service = V1beta1InferenceService(
        api_version=constants.KSERVE_V1BETA1,
        kind=constants.KSERVE_KIND,
        metadata={"name": model_name, "namespace": namespace},
        spec=V1beta1InferenceServiceSpec(
            predictor=V1beta1PredictorSpec(
                sklearn=V1beta1SKLearnSpec(
                    storage_uri=f"s3://{model_bucket}/{model_key}",
                    env=[
                        {"name": "AWS_ACCESS_KEY_ID", "value": minio_access_key},
                        {"name": "AWS_SECRET_ACCESS_KEY", "value": minio_secret_key},
                        {"name": "AWS_ENDPOINT_URL", "value": f"http://{minio_endpoint}"},
                        {"name": "AWS_S3_FORCE_PATH_STYLE", "value": "true"},
                    ],
                )
            )
        )
    )

    # Deploy the InferenceService
    try:
        kserve_client.create(inference_service)
        print(f"InferenceService '{model_name}' deployed successfully.")
        status = "Success"
    except Exception as e:
        print(f"Failed to deploy InferenceService: {e}")
        status = "Failed"

    # Return outputs
    output = namedtuple('Outputs', ['inference_service_name', 'status'])
    return output(model_name, status)
 
 
 
 
 



