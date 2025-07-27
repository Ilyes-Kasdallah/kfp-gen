import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics

# Define the pipeline function name
data_ingest_fns = "data_ingestion_pipeline"


# Define the pipeline
@pipeline(name=data_ingest_fns)
def data_ingestion_pipeline(
    df_path: Input[Dataset],
    to_keep: List[str],
    data: str,
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the CSV dataset
    df = kfp.components.load_dataset(df_path)

    # Filter the dataset based on the specified columns
    filtered_df = df.select(columns=to_keep)

    # Check if the data is for training or serving
    if data == "train":
        # Split the dataset into training and validation sets
        train_val_split = filtered_df.split(test_size=0.2, random_state=42)
        train_df, val_df = train_val_split

        # Save the training and validation datasets
        train_dataset = kfp.components.save_dataset(train_df, "train_dataset")
        val_dataset = kfp.components.save_dataset(val_df, "val_dataset")

        # Create a model for training
        model = kfp.components.create_model("model", "mlp", train_dataset)

        # Train the model
        model.train()

        # Save the trained model
        model.save("model")

        # Return the model
        return model
    else:
        # Load the dataset
        df = kfp.components.load_dataset(df_path)

        # Predict the labels for the given data
        predictions = df["target_column"].apply(lambda x: model.predict(x))

        # Save the predictions
        predictions_df = kfp.components.save_dataset(predictions, "predictions")

        # Return the predictions
        return predictions_df
