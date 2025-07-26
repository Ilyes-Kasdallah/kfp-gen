import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="Additional Packages Pipeline")
def additional_packages_pipeline():
    # Define the get_iris_data component
    @component
    def get_iris_data():
        # Load the Iris dataset
        iris = kfp.data.Dataset.from_pandas(kfp.io.csv.read_csv("data/iris.csv"))

        # Convert the dataset into a Pandas DataFrame
        df = iris.to_pandas()

        # Print the head of the DataFrame
        print(df.head())

        # Return the DataFrame
        return df


# Execute the pipeline
additional_packages_pipeline().execute()
