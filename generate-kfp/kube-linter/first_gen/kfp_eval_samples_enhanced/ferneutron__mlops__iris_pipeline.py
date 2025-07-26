import kfp
from kfp.dsl import pipeline, component

# Import necessary libraries
from google.cloud import bigquery


@component
def load_data_from_bigquery(project_id: str, bq_dataset: str, bq_table: str) -> tuple:
    """
    Load data from BigQuery into a specified dataset.

    Args:
    project_id (str): The ID of the Google Cloud project.
    bq_dataset (str): The name of the BigQuery dataset.
    bq_table (str): The name of the BigQuery table.

    Returns:
    tuple: A tuple containing the train and test datasets.
    """
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{bq_dataset}.{bq_table}`"
    df = client.query(query).to_dataframe()
    return df


@pipeline(name="The-Iris-Pipeline-v1")
def iris_pipeline(
    project_id: str,
    bq_dataset: str,
    bq_table: str,
    train_dataset: str,
    test_dataset: str,
    num_epochs: int = 5,
    batch_size: int = 32,
    learning_rate: float = 0.01,
    dropout_rate: float = 0.1,
    validation_split: float = 0.2,
    model_name: str = "iris_model",
    hyperparameters: dict = {
        "learning_rate": learning_rate,
        "dropout_rate": dropout_rate,
        "batch_size": batch_size,
        "num_epochs": num_epochs,
        "validation_split": validation_split,
    },
):
    """
    Create a pipeline to perform machine learning on the Iris dataset.

    Args:
    project_id (str): The ID of the Google Cloud project.
    bq_dataset (str): The name of the BigQuery dataset.
    bq_table (str): The name of the BigQuery table.
    train_dataset (str): The name of the train dataset.
    test_dataset (str): The name of the test dataset.
    num_epochs (int): Number of epochs for training.
    batch_size (int): Batch size for training.
    learning_rate (float): Learning rate for training.
    dropout_rate (float): Dropout rate for training.
    validation_split (float): Validation split for training.
    model_name (str): Name of the model to use.
    hyperparameters (dict): Hyperparameters to be used in the model.

    Returns:
    None
    """
    # Load data from BigQuery
    df = load_data_from_bigquery(project_id, bq_dataset, bq_table)

    # Split the data into training and testing sets
    train_df, test_df = df.sample(frac=0.8), df.sample(frac=0.2)

    # Define the model
    model = kfp.components.load_component(
        "iris_model", package_path="path/to/iris_model"
    )

    # Train the model
    model.fit(
        train_df,
        epochs=num_epochs,
        batch_size=batch_size,
        hyperparameters=hyperparameters,
    )

    # Evaluate the model
    model.evaluate(test_df)


# Example usage
iris_pipeline(
    project_id="your-project-id",
    bq_dataset="your-bq-dataset",
    bq_table="your-bq-table",
    train_dataset="train_dataset",
    test_dataset="test_dataset",
    num_epochs=10,
    batch_size=32,
    learning_rate=0.01,
    dropout_rate=0.1,
    validation_split=0.2,
    model_name="iris_model",
    hyperparameters={
        "learning_rate": learning_rate,
        "dropout_rate": dropout_rate,
        "batch_size": batch_size,
        "num_epochs": num_epochs,
        "validation_split": validation_split,
    },
)
