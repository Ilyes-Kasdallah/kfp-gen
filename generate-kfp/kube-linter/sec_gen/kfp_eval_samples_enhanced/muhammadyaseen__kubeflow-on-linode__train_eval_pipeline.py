import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="train_eval_pipeline")
def train_eval_pipeline():
    # Define the training baseline model component
    train_eval_baseline_model = component(
        name="train_eval_baseline_model",
        description="Trains multiple baseline models.",
        inputs=[Input("data", type=Input.Dataset), Input("labels", type=Input.Dataset)],
        outputs=[Output("model", type=Output.Model)],
        steps=[
            component(
                name="baseline_model_train",
                description="Trains a baseline model.",
                inputs=[
                    Input("data", type=Input.Dataset),
                    Input("labels", type=Input.Dataset),
                ],
                outputs=[Output("model", type=Output.Model)],
                steps=[
                    component(
                        name="baseline_model_predict",
                        description="Predicts labels for the given data.",
                        inputs=[
                            Input("model", type=Input.Model),
                            Input("data", type=Input.Dataset),
                        ],
                        outputs=[Output("predictions", type=Output.Dataset)],
                    )
                ],
            )
        ],
    )

    # Define the evaluation pipeline component
    evaluate_pipeline = component(
        name="evaluate_pipeline",
        description="Evaluates the trained model.",
        inputs=[
            Input("model", type=Input.Model),
            Input("test_data", type=Input.Dataset),
        ],
        outputs=[Output("metrics", type=Output.Metrics)],
        steps=[
            component(
                name="evaluate_model",
                description="Evaluates the model's performance on the test data.",
                inputs=[
                    Input("model", type=Input.Model),
                    Input("test_data", type=Input.Dataset),
                ],
                outputs=[Output("metrics", type=Output.Metrics)],
            )
        ],
    )

    # Define the pipeline root parameter
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Return the pipeline function
    return pipeline(
        name="train_eval_pipeline",
        description="Runs the training and evaluation pipelines.",
        steps=[train_eval_baseline_model, evaluate_pipeline],
        output_dir=pipeline_root,
    )
