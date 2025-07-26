
from kubeflow.pipelines import dsl

@dsl.pipeline(name="Default")
def default():
    # Start component
    start = dsl.component(
        name="Start",
        image="busybox",
        init_container={
            "command": ["echo", "Pipeline starting"],
            "name": "Training Started"
        }
    )

    # Send callback message to kubemlopsbot-svc.kubeflow.svc.cluster.local:8080
    send_callback = dsl.component(
        name="SendCallback",
        image="curl",
        command=["curl", "-X POST", "http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080/callback"]
    )

    # Connect components
    start >> send_callback
