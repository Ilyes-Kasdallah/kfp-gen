from kfp import pipeline
from kfp.dsl import component
import minio


@component
def check_if_raw_data_exists_already(bucket_name: str, object_name: str) -> bool:
    """
    Checks if raw data (specified by object_name) already exists in a Minio bucket.

    Args:
    - bucket_name (str): The name of the Minio bucket.
    - object_name (str): The name of the object to check.

    Returns:
    - bool: True if the object exists, False otherwise.
    """
    try:
        minio_client = minio.Minio(bucket_name)
        return minio_client.exists(object_name)
    except Exception as e:
        print(f"Error checking if object exists: {e}")
        return False


@pipeline(name="cleaning_and_prep_pipeline")
def cleaning_and_prep_pipeline():
    """
    A pipeline that performs data cleaning and preparation.

    Steps:
    1. Check if raw data (specified by 'object_name') exists in 'bucket_name'.
    2. If the object does not exist, proceed to cleaning and preparing.
    3. Clean and prepare the data.
    """
    # Step 1: Check if raw data exists
    if not check_if_raw_data_exists_already("your_bucket_name", "your_object_name"):
        raise ValueError("Raw data does not exist in the specified bucket.")

    # Step 2: Perform cleaning and preparation
    # Example: Load data from a CSV file, perform some transformations, etc.
    # This is a placeholder for actual data processing logic
    cleaned_data = "Processed data"

    # Step 3: Prepare the data
    # Example: Save the cleaned data to a new CSV file
    # This is a placeholder for actual data preparation logic
    prepared_data = "Prepared data"

    # Output the results
    print("Cleaned Data:", cleaned_data)
    print("Prepared Data:", prepared_data)


# Run the pipeline
cleaning_and_prep_pipeline()
