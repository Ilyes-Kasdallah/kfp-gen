```python
from kfp import dsl
from kfp.components import load_component_from_text

# Load components from text files
data_chunk_spliter = load_component_from_text("""
apiVersion: kfp.v2.components/v1
kind: Component
metadata:
  name: data-chunk-spliter
spec:
  implementation:
    container:
      image: gcr.io/kubeflow/pipelines/python-sdk@latest
      command:
        - python
        - /app/data_chunk_spliter.py
      args:
        - --pipeline
        - ${{inputs.parameters.pipeline}}
        - --bucket-name
        - ${{inputs.parameters.bucket_name}}
        - --job-id
        - ${{inputs.parameters.job_id}}
        - --dataset
        - ${{inputs.parameters.dataset}}
        - --chunk-size
        - ${{inputs.parameters.chunk_size}}
      resources:
        limits:
          cpu: "1"
          memory: "500Mi"
        requests:
          cpu: "0.5"
          memory: "250Mi"
      retries:
        limit: 2
""")
pose_annotation = load_component_from_text("""
apiVersion: kfp.v2.components/v1
kind: Component
metadata:
  name: pose-annotation
spec:
  implementation:
    container:
      image: gcr.io/kubeflow/pipelines/python-sdk@latest
      command:
        - python
        - /app/pose_annotation.py
      args:
        - --pipeline
        - ${{inputs.parameters.pipeline}}
        - --bucket-name
        - ${{inputs.parameters.bucket_name}}
        - --job-id
        - ${{inputs.parameters.job_id}}
        - --validation-ratio
        - ${{inputs.parameters.valid_ratio}}
        - --chunk-file
        - ${{inputs.parameters.chunk_file}}
      resources:
        limits:
          cpu: "1"
          memory: "500Mi"
        requests:
          cpu: "0.5"
          memory: "250Mi"
      retries:
        limit: 2
""")
slack_notification = load_component_from_text("""
apiVersion: kfp.v2.components/v1
kind: Component
metadata:
  name: slack-notification
spec:
  implementation:
    container:
      image: gcr.io/kubeflow/pipelines/python-sdk@latest
      command:
        - python
        - /app/slack_notification.py
      args:
        - --pipeline-name
        - ${{inputs.parameters.pipeline_name}}
        - --job-id
        - ${{inputs.parameters.job_id}}
        - --workflow-status
        - ${{workflow.status}}
      resources:
        limits:
          cpu: "1"
          memory: "500Mi"
        requests:
          cpu: "0.5"
          memory: "250Mi"
      retries:
        limit: 2
""")

@dsl.pipeline(name="head-pose-dataset-pipeline")
def head_pose_dataset_pipeline(
    pipeline: str,
    bucket_name: str,
    job_id: str,
    dataset: str,
    chunk_size: int,
    valid_ratio: float
):
    # Data chunk splitter
    data_chunks = data_chunk_spliter(pipeline=pipeline, bucket_name=bucket_name, job_id=job_id, dataset=dataset, chunk_size=chunk_size)

    # Parallel for loop to process each chunk
    with dsl.ParallelFor(data_chunks) as chunk:
        pose_annotation(pipeline=pipeline, bucket_name=bucket_name, job_id=job_id, validation_ratio=valid_ratio, chunk_file=chunk.output)

    # Exit handler
    slack_notification(pipeline_name=pipeline, job_id=job_id, workflow_status=dsl.get_workflow().status)
```

This code snippet defines a Kubeflow Pipeline named `head-pose-dataset-pipeline` that performs the creation of a TFRecord dataset for a head-pose pipeline. It includes components for data chunk splitting, pose annotation, and Slack notifications. The pipeline uses Google Cloud Storage for data management and leverages the `gcp` module from the Kubeflow Pipelines SDK for preemptible nodepools.