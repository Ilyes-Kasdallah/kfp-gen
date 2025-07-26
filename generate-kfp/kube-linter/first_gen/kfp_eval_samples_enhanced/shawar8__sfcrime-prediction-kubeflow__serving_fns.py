import kfp
from kfp.dsl import pipeline, component

# Import necessary libraries
import sodapy
import pandas as pd

# Define the pipeline function name
pipeline_name = "Serving Pipeline"


# Define the get_data component
@component
def get_data():
    # Retrieve crime incident data from the San Francisco Open Data portal
    url = "https://data.sfdp.org/api/v2/Incidents?start_date=2023-04-01&end_date=2023-04-30"
    response = sodapy.read(url)
    df = pd.DataFrame(response)
    return df


# Define the serving_fns component
@component
def serving_fns(df):
    # Transform the data by filtering out non-incident crimes
    filtered_df = df[df["IncidentType"] == "Non-Incident"]
    return filtered_df


# Define the main function to orchestrate the pipeline
@pipeline(name=pipeline_name)
def main():
    # Get data from the San Francisco Open Data portal
    data = get_data()

    # Transform the data
    transformed_data = serving_fns(data)

    # Serve the transformed data
    # This is a placeholder for serving logic
    print("Transformed Data:", transformed_data)


# Run the pipeline
if __name__ == "__main__":
    main()
