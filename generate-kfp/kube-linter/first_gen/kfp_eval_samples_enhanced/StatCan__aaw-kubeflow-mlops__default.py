from kfp import components
from kfp.dsl import pipeline


@pipeline(name="Default")
def default():
    # Start component
    start = components.Start(
        image="busybox",
        command=["echo", "Pipeline starting"],
        init_container=components.InitContainer(
            command=[
                "curl",
                "-X",
                "POST",
                "http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080/training_started",
            ]
        ),
    )

    # Component to send callback messages
    send_callback = components.Component(
        name="send_callback",
        image="busybox",
        command=[
            "echo",
            "Callback sent to kubemlopsbot-svc.kubeflow.svc.cluster.local:8080",
        ],
    )

    # Connect the two components
    start >> send_callback


# Run the pipeline
default()
