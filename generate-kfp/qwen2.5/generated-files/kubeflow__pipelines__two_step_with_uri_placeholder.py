
from kfp import dsl

@dsl.pipeline(name="two-step-with-uri-placeholders")
def two_step_with_uri_placeholder():
    # Step 1: Create a pipeline component that uses a URI placeholder
    create_pipeline_component = dsl.component(
        name="create_pipeline_component",
        description="Creates a pipeline component with a URI placeholder",
        steps=[
            dsl.task(
                name="task1",
                description="Task 1",
                image="gcr.io/kubeflow/pipelines:latest",
                command=["echo", "Hello from Task 1"],
                uri_placeholder="https://example.com/data"
            ),
            dsl.task(
                name="task2",
                description="Task 2",
                image="gcr.io/kubeflow/pipelines:latest",
                command=["echo", "Hello from Task 2"],
                uri_placeholder="https://example.com/data"
            )
        ]
    )

    # Step 2: Use the created pipeline component in another pipeline
    use_pipeline_component = dsl.component(
        name="use_pipeline_component",
        description="Uses the created pipeline component",
        steps=[
            dsl.task(
                name="task3",
                description="Task 3",
                image="gcr.io/kubeflow/pipelines:latest",
                command=["echo", "Hello from Task 3"],
                uri_placeholder="https://example.com/data"
            )
        ]
    )

    return create_pipeline_component, use_pipeline_component
