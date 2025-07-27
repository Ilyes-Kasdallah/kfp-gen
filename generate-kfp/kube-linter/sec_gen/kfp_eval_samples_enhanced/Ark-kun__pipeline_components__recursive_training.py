import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the recursive_training function
@dsl.component(name="recursive_training")
def recursive_training(
    input_data: Dataset,
    model: Model,
    epochs: int = 10,
    learning_rate: float = 0.01,
    batch_size: int = 32,
    validation_split: float = 0.2,
    max_epochs: int = 100,
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the dataset
    df = input_data.read_csv()

    # Split the dataset into training and validation sets
    train_df, val_df = df.split(df.shape[0] * validation_split)

    # Train the model
    model.fit(
        train_df,
        epochs=epochs,
        learning_rate=learning_rate,
        batch_size=batch_size,
        validation_split=validation_split,
        max_epochs=max_epochs,
        cache=cache,
    )

    # Evaluate the model on the validation set
    metrics = model.evaluate(val_df)

    # Save the model
    model.save("model")

    # Return the metrics
    return metrics


# Define the pipeline
@dsl.pipeline(name="train_until_good_pipeline")
def train_until_good_pipeline(
    input_data: Dataset,
    model: Model,
    epochs: int = 10,
    learning_rate: float = 0.01,
    batch_size: int = 32,
    validation_split: float = 0.2,
    max_epochs: int = 100,
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the dataset
    df = input_data.read_csv()

    # Split the dataset into training and validation sets
    train_df, val_df = df.split(df.shape[0] * validation_split)

    # Train the model
    model.fit(
        train_df,
        epochs=epochs,
        learning_rate=learning_rate,
        batch_size=batch_size,
        validation_split=validation_split,
        max_epochs=max_epochs,
        cache=cache,
    )

    # Evaluate the model on the validation set
    metrics = model.evaluate(val_df)

    # Save the model
    model.save("model")

    # Return the metrics
    return metrics


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(
    train_until_good_pipeline, pipeline_root=pipeline_root
)
