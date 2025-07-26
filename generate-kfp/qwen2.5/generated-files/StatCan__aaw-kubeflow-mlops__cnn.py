
from kubeflow.pipelines import dsl

@dsl.pipeline(name="Tacos vs. Burritos")
def tacos_vs_burritos():
    # Define the components
    exit_handler = dsl.component(
        name="Exit Handler",
        description="Send completion message to Kubemlopsbot-svc",
        steps=[
            dsl.http_request(
                url="http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080",
                method="POST",
                body={"status": "completed"},
                headers={"Content-Type": "application/json"}
            )
        ]
    )

    # Define the CNN component
    cnn = dsl.component(
        name="CNN",
        description="Convolutional Neural Network",
        steps=[
            dsl.http_request(
                url="http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080",
                method="POST",
                body={"model": "cnn"},
                headers={"Content-Type": "application/json"}
            )
        ]
    )

    # Define the main component
    main = dsl.component(
        name="Main",
        description="Run the CNN component",
        steps=[
            exit_handler,
            cnn
        ]
    )

    # Return the main component
    return main
