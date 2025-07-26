import snowflake.connector
from google.cloud import storage


@dsl.pipeline(name="snowflake_data_unload")
def snowflake_data_unload():
    # Define the Snowflake connection parameters
    conn_params = {
        "account": "your_account",
        "database": "your_database",
        "username": "your_username",
        "password": "your_password",
    }

    # Define the GCS bucket parameters
    gcs_bucket_name = "your_gcs_bucket"

    # Create a Snowflake connector instance
    conn = snowflake.connector.connect(**conn_params)

    # Define the SQL query to load data from Snowflake
    sql_query = """
    SELECT *
    FROM your_table
    """

    # Execute the SQL query and store the result in a DataFrame
    df = conn.execute(sql_query).fetchall()

    # Define the Google Cloud Storage client
    storage_client = storage.Client()

    # Define the destination path in GCS
    destination_path = f"gs://{gcs_bucket_name}/{df[0]['column_name']}"

    # Upload the DataFrame to GCS
    blob = storage_client.blob(destination_path)
    blob.upload_from_dataframe(df)

    # Close the connection to the Snowflake database
    conn.close()
