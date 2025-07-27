import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="metrics_visualization_v2")
def metrics_visualization_v2():
    # Define the first task: digit_classification
    @dsl.component(name="digit_classification")
    def digit_classification(
        iris_data: Dataset[Input[Dataset]],
        model: Model[Output[Model]],
        num_epochs: int = 10,
        batch_size: int = 32,
        learning_rate: float = 0.01,
        validation_split: float = 0.2,
    ) -> Model:
        # Load the Iris dataset
        iris = kfp.components.load_dataset("iris")

        # Split the dataset into training and testing sets
        train, test = iris.split(test_size=validation_split)

        # Train the model
        model.fit(train)

        # Evaluate the model
        metrics = model.evaluate(test)

        # Save the model
        model.save()

        return model

    # Define the second task: logging_metrics
    @dsl.component(name="logging_metrics")
    def logging_metrics(
        model: Model[Output[Model]],
        metrics: Metrics,
        log_dir: Output[Dataset[Input[Dataset]]] = None,
    ) -> None:
        # Log the model metrics to a directory
        if log_dir is not None:
            model.log_metrics(log_dir)


# Run the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
pipeline = metrics_visualization_v2(pipeline_root=pipeline_root)
pipeline.run()
