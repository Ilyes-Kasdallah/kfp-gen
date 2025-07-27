import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="metrics_visualization_v2")
def metrics_visualization_v2():
    # Define the first task: digit_classification
    @dsl.component(name="digit_classification")
    def digit_classification(
        input_dataset: Dataset[Input[Dataset]], output_model: Model[Output[Model]]
    ) -> None:
        # Load the Iris dataset
        iris = kfp.components.load_dataset("iris")

        # Perform digit classification
        model = kfp.components.predict(iris, model_name="digit-classification")

        # Save the model
        model.save(output_model)

    # Define the second task: logging_metrics
    @dsl.component(name="logging_metrics")
    def logging_metrics(
        input_dataset: Dataset[Input[Dataset]], output_metrics: Metrics[Output[Metrics]]
    ) -> None:
        # Log the metrics
        metrics = kfp.components.log_metrics(input_dataset, output_metrics)
        metrics.save(output_metrics)


# Run the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
pipeline = metrics_visualization_v2()
pipeline.run(pipeline_root=pipeline_root)
