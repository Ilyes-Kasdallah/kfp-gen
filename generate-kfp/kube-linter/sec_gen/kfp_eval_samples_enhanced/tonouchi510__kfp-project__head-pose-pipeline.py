import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the Training Component
@component
def training(
    input_dataset: Dataset,
    model: Model,
    metrics: Metrics,
    num_epochs: int = 10,
    learning_rate: float = 0.01,
    batch_size: int = 32,
    cache_dir: str = None,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the dataset
    data = input_dataset.read_csv()

    # Train the model
    model.fit(
        data, epochs=num_epochs, learning_rate=learning_rate, batch_size=batch_size
    )

    # Evaluate the model
    metrics = model.evaluate(data)

    # Save the model
    model.save("model")

    # Return the metrics
    return metrics


# Define the Evaluation Component
@component
def evaluation(
    input_dataset: Dataset,
    model: Model,
    metrics: Metrics,
    output_dataset: Dataset,
    cache_dir: str = None,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the dataset
    data = input_dataset.read_csv()

    # Evaluate the model
    metrics = model.evaluate(data)

    # Save the results
    output_dataset.write_csv(metrics)

    # Return the metrics
    return metrics


# Define the Pipeline Function
@pipeline(name="head-pose-pipeline")
def head_pose_pipeline(
    input_dataset: Dataset,
    model: Model,
    metrics: Metrics,
    num_epochs: int = 10,
    learning_rate: float = 0.01,
    batch_size: int = 32,
    cache_dir: str = None,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Training
    training_result = training(
        input_dataset,
        model,
        metrics,
        num_epochs,
        learning_rate,
        batch_size,
        cache_dir,
        retries,
        resource_limits,
    )

    # Evaluation
    evaluation_result = evaluation(
        training_result,
        model,
        metrics,
        output_dataset,
        cache_dir,
        retries,
        resource_limits,
    )

    return evaluation_result


# Compile the Pipeline
kfp.compiler.Compiler().compile(head_pose_pipeline)
