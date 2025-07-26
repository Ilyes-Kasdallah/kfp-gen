
from kfp import dsl

@dsl.pipeline(name="cleaning_and_prep_pipeline")
def cleaning_and_prep_pipeline(object_name, bucket_name):
    # Define the component to check if raw data exists
    @dsl.component
    def check_if_raw_data_exists_already(bucket_name, object_name):
        # Connect to Minio
        minio_client = dsl.connect_to_minio(bucket_name)
        
        # Check if the object exists
        try:
            minio_client.get_object(object_name)
            return True
        except Exception as e:
            print(f"Error checking if object {object_name} exists: {e}")
            return False

    # Define the component to perform data cleaning and preparation
    @dsl.component
    def clean_and_prep(object_name, bucket_name):
        # Check if raw data exists
        if not check_if_raw_data_exists_already(bucket_name, object_name):
            raise ValueError("Raw data does not exist in Minio.")
        
        # Perform data cleaning and preparation
        # Example: Load data from Minio, perform transformations, etc.
        # Here, we'll just print the object name for demonstration purposes
        print(f"Cleaning and preparing object {object_name}...")
        
        # Return the cleaned and prepared object name
        return object_name

# Example usage
cleaning_and_prep_pipeline("example_object", "minio_bucket")
