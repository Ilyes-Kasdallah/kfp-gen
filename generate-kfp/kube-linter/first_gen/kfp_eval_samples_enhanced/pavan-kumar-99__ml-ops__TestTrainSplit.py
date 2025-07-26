import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from kfp.components import getRawData


@pipeline(name="DataSplitPipeline")
def DataSplitPipeline():
    # Define the getRawData component
    @component
    def getRawData():
        # Load data from a remote YAML file
        raw_data = getRawData()
        # Return the file path to the downloaded dataset
        return raw_data

    # Define the TestTrainSplit function
    @component
    def TestTrainSplit(raw_data_path):
        # Split the dataset into training and testing sets
        # Example: Split by a specific column
        # Assuming 'target_column' is the column to split by
        # train_set, test_set = split_dataset(raw_data_path, target_column)
        # Return the paths of the training and testing sets
        return train_set, test_set


# Example usage
if __name__ == "__main__":
    # Call the TestTrainSplit function with the path to the downloaded dataset
    train_set, test_set = TestTrainSplit("path/to/downloaded/dataset.csv")
    print(f"Training set: {train_set}")
    print(f"Testing set: {test_set}")
