
from kfp import dsl

@dsl.pipeline(name="Additional Packages Pipeline")
def AdditionalPackagesPipeline():
    # Define the get_iris_data component
    @dsl.component
    def get_iris_data():
        # Load the Iris dataset from scikit-learn
        iris = load_iris()
        
        # Convert the dataset into a Pandas DataFrame
        df = iris.to_pandas()
        
        # Print the head of the DataFrame
        print(df.head())

# Define the load_iris function
def load_iris():
    # Import the necessary libraries
    import numpy as np
    from sklearn.datasets import load_iris
    
    # Load the Iris dataset
    iris = load_iris()
    
    # Return the dataset as a Pandas DataFrame
    return iris.data

# Call the AdditionalPackagesPipeline function
AdditionalPackagesPipeline()
