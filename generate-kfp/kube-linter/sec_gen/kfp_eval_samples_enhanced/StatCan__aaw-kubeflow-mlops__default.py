import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@component
def Start():
    """Start component."""
    print("Pipeline starting")
    # Send a "Training Started" event to kubemlopsbot-svc.kubeflow.svc.cluster.local:8080 via a curl command
    curl_command = f"curl -X POST http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080/training_started"
    print(curl_command)
    return None


@component
def Train():
    """Train component."""
    # Simulate training logic here
    print("Training started")
    # Example of training logic
    return None


@component
def Callback():
    """Callback component."""
    """Send callback messages to a URL."""
    url = "http://example.com/callback"
    print(f"Sending callback to {url}")
    return None


@pipeline(name="Default", description="Simple training pipeline")
def Default():
    """Default pipeline."""
    start_task = Start()
    train_task = Train()
    callback_task = Callback()

    # Define dependencies between tasks
    start_task >> train_task >> callback_task

    return None


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(Default, pipeline_root)
print(compiled_pipeline)
