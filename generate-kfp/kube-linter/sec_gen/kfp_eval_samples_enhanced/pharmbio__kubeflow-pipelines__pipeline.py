import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Kensert_CNN_test")
def Kensert_CNN_test(
    model_type="Inception_v3",
    checkpoint_preprocess=True,
    workspace_name="gs://my-bucket/pipeline-root",
):
    # Define the preprocessing component
    preprocess_component = component(
        name="preprocessing",
        description="Preprocesses the input data.",
        inputs={
            "model_type": Input(type="string", default="Inception_v3"),
            "checkpoint_preprocess": Input(type="bool", default=True),
            "workspace_name": Input(
                type="string", default="gs://my-bucket/pipeline-root"
            ),
        },
        outputs={
            "processed_data": Output(type="Dataset", description="The processed data."),
        },
        steps=[
            component(
                name="load_data",
                description="Loads the input data.",
                inputs={
                    "dataset_path": Input(type="string"),
                },
                outputs={
                    "data": Output(type="Dataset", description="The loaded data."),
                },
            ),
            component(
                name="preprocess_data",
                description="Preprocesses the data.",
                inputs={
                    "data": Input(type="Dataset", description="The loaded data."),
                    "model_type": Input(type="string", default="Inception_v3"),
                    "checkpoint_preprocess": Input(type="bool", default=True),
                    "workspace_name": Input(
                        type="string", default="gs://my-bucket/pipeline-root"
                    ),
                },
                outputs={
                    "processed_data": Output(
                        type="Dataset", description="The processed data."
                    ),
                },
            ),
        ],
    )

    # Define the model component
    model_component = component(
        name="model",
        description="Creates a model.",
        inputs={
            "model_type": Input(type="string", default="Inception_v3"),
            "checkpoint_preprocess": Input(type="bool", default=True),
            "workspace_name": Input(
                type="string", default="gs://my-bucket/pipeline-root"
            ),
        },
        outputs={
            "model": Output(type="Model", description="The created model."),
        },
        steps=[
            component(
                name="load_model",
                description="Loads the model.",
                inputs={
                    "model_path": Input(type="string"),
                },
                outputs={
                    "model": Output(type="Model", description="The loaded model."),
                },
            ),
        ],
    )

    # Define the metrics component
    metrics_component = component(
        name="metrics",
        description="Calculates metrics.",
        inputs={
            "model": Input(type="Model", description="The model to evaluate."),
            "checkpoint_preprocess": Input(type="bool", default=True),
            "workspace_name": Input(
                type="string", default="gs://my-bucket/pipeline-root"
            ),
        },
        outputs={
            "metrics": Output(type="Metrics", description="The calculated metrics."),
        },
        steps=[
            component(
                name="evaluate_model",
                description="Evaluates the model.",
                inputs={
                    "model": Input(type="Model", description="The model to evaluate."),
                    "checkpoint_preprocess": Input(type="bool", default=True),
                    "workspace_name": Input(
                        type="string", default="gs://my-bucket/pipeline-root"
                    ),
                },
                outputs={
                    "metrics": Output(
                        type="Metrics", description="The evaluated metrics."
                    ),
                },
            ),
        ],
    )

    # Define the pipeline
    pipeline = pipeline(
        name="Kensert_CNN_test",
        description="Runs a CNN workflow.",
        steps=[
            preprocess_component,
            model_component,
            metrics_component,
        ],
    )

    # Enable caching
    pipeline.enable_caching()

    # Set retries
    pipeline.set_retries(2)

    # Set resource limits
    pipeline.resource_limits(
        cpu="1",
        memory="1Gi",
    )

    # Return the pipeline
    return pipeline
