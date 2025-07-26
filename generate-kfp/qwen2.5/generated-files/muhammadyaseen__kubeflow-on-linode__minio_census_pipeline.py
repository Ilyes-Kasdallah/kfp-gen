
from kfp import dsl

@dsl.pipeline(name="census_data_pipeline")
def census_data_pipeline():
    # Define the MinIO bucket name
    minio_bucket_name = "census_data"
    
    # Define the MinIO client
    minio_client = dsl.MinIOClient.from_env(
        access_key="your_access_key",
        secret_key="your_secret_key",
        region_name="your_region"
    )
    
    # Define the component to check if table data exists
    @dsl.component(name="check_if_table_data_exists_already")
    def check_if_table_data_exists_already(bucket_name):
        # Check if the table data exists in the MinIO bucket
        try:
            # Retrieve the table data from MinIO
            table_data = minio_client.get_object(bucket_name, "table_data.csv")
            return True
        except Exception as e:
            print(f"Error checking table data: {e}")
            return False
    
    # Define the component to download table data from the Census API
    @dsl.component(name="download_table_data_from_census_api")
    def download_table_data_from_census_api(table_data_url):
        # Download the table data from the Census API
        try:
            # Send a GET request to the Census API
            response = requests.get(table_data_url)
            response.raise_for_status()  # Raise an error for bad responses
            table_data = response.text
            return table_data
        except requests.exceptions.RequestException as e:
            print(f"Error downloading table data: {e}")
            return None
    
    # Define the main task of the pipeline
    @dsl.task(name="main_task")
    def main_task():
        # Check if table data exists in MinIO
        table_exists = check_if_table_data_exists_already(minio_bucket_name)
        
        # If table data exists, download it from the Census API
        if table_exists:
            table_data = download_table_data_from_census_api("https://api.census.gov/data/v3/2021/acs/acs10/s10001001")
            print(f"Table data downloaded successfully: {table_data}")
        else:
            print("Table data does not exist in MinIO.")
    
    # Run the main task
    main_task()
