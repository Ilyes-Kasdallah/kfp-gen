from kfp import pipeline
from kfp.dsl import component
import minio


@component
def check_if_table_data_exists_already(
    minio_client: minio.Client, bucket_name: str, table_name: str
) -> bool:
    """
    Checks if the specified table data exists in the MinIO bucket.

    Args:
    minio_client (minio.Client): The MinIO client used to interact with the bucket.
    bucket_name (str): The name of the MinIO bucket.
    table_name (str): The name of the table to check.

    Returns:
    bool: True if the table data exists, False otherwise.
    """
    # Check if the table exists in the bucket
    try:
        minio_client.head_object(bucket_name, table_name)
        return True
    except minio.errors.NoSuchKeyError:
        return False


@pipeline(name="census_data_pipeline")
def census_data_pipeline():
    """
    Processes Census data by checking for its existence in MinIO storage and downloading it from the Census API if needed.
    """
    # Define the bucket and table names
    bucket_name = "census_data"
    table_name = "people"

    # Check if the table data exists
    table_exists = check_if_table_data_exists_already(
        minio_client=minio.Client(), bucket_name=bucket_name, table_name=table_name
    )

    # Download the table data if it exists
    if table_exists:
        # Assume the table data is stored in a specific format
        # For demonstration, let's assume it's in CSV format
        csv_file_path = f"{bucket_name}/{table_name}.csv"
        # Download the CSV file
        minio_client.download_object(bucket_name, table_name, csv_file_path)

        print(f"Table data downloaded successfully: {csv_file_path}")
    else:
        print("Table data does not exist in the specified bucket.")


# Run the pipeline
census_data_pipeline()
