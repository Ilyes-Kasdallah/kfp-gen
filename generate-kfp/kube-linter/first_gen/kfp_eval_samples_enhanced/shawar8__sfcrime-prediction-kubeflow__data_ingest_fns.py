import kfp
from kfp.dsl import pipeline, component

# Define the pipeline function name
data_ingest_fns = "data_ingestion_pipeline"


@dsl.pipeline(name=data_ingest_fns)
def data_ingestion_pipeline(
    df_path: str,
    to_keep: list[str],
    data: str = "train",
):
    """
    Data ingestion pipeline for crime dataset.

    Args:
    - df_path (str): Path to the CSV dataset.
    - to_keep (list[str]): List of columns to keep in the dataset.
    - data (str): Determines whether the data is for training or serving.

    Returns:
    - None
    """
    # Import necessary modules
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    # Load the dataset
    df = pd.read_csv(df_path)

    # Check if the data is for training or serving
    if data == "train":
        X = df.drop(columns=to_keep)
        y = df["target_column"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
    else:
        X = df.drop(columns=to_keep)
        y = df["target_column"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

    # Save the processed data
    X_train.to_csv("X_train.csv", index=False)
    X_test.to_csv("X_test.csv", index=False)
