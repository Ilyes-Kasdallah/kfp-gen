import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_v2_test():
    # Define the wine-classification component
    wine_classification = component(
        name="wine-classification",
        description="Perform wine classification.",
        inputs={
            "data": Input(Dataset("wine_data.csv")),
        },
        outputs={
            "metrics": Output(Metrics()),
        },
        steps=[
            component(
                name="train_model",
                description="Train a model on the wine dataset.",
                inputs={
                    "data": Input(Dataset("wine_data.csv")),
                },
                outputs={
                    "model": Output(Model()),
                },
                steps=[
                    component(
                        name="evaluate_model",
                        description="Evaluate the model's performance.",
                        inputs={
                            "model": Input(Model()),
                            "test_data": Input(Dataset("wine_test.csv")),
                        },
                        outputs={
                            "metrics": Output(Metrics()),
                        },
                    ),
                ],
            ),
            component(
                name="visualize_metrics",
                description="Visualize the model's performance metrics.",
                inputs={
                    "model": Input(Model()),
                    "metrics": Input(Metrics()),
                },
                outputs={
                    "visualization": Output(Dataset("wine_metrics.png")),
                },
            ),
        ],
    )

    # Call the wine-classification component
    wine_classification()


# Compile the pipeline
kfp.compiler.Compiler().compile(metrics_visualization_v2_test)
