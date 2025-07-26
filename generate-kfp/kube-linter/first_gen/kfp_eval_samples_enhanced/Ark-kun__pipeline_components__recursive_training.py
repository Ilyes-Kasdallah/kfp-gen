import kfp
from kfp.dsl import (
    pipeline,
    component,
    Input,
    Output,
    Dataset,
    PipelineArgument,
    KubernetesJob,
)

# Import necessary modules
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from pandas import read_csv, DataFrame


# Define the recursive_training function
@component
def recursive_training(
    input_data: Dataset[str],
    target_column: str,
    learning_rate: float,
    max_depth: int,
    num_estimators: int,
    early_stopping_rounds: int,
    validation_split: float,
    error_threshold: float,
) -> DataFrame:
    # Load the dataset
    data = read_csv(input_data)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data, target_column, test_size=validation_split, random_state=42
    )

    # Initialize the XGBoost classifier
    model = XGBClassifier(
        learning_rate=learning_rate,
        max_depth=max_depth,
        num_estimators=num_estimators,
        early_stopping_rounds=early_stopping_rounds,
    )

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)

    # Check if the accuracy is below the error threshold
    if accuracy < error_threshold:
        raise ValueError(f"Model accuracy is below the error threshold: {accuracy}")

    return model


# Define the train_until_good_pipeline function
@pipeline(name="train_until_good_pipeline")
def train_until_good_pipeline(
    input_data: Dataset[str],
    target_column: str,
    learning_rate: float,
    max_depth: int,
    num_estimators: int,
    early_stopping_rounds: int,
    validation_split: float,
    error_threshold: float,
) -> DataFrame:
    # Call the recursive_training function
    try:
        result = recursive_training(
            input_data=input_data,
            target_column=target_column,
            learning_rate=learning_rate,
            max_depth=max_depth,
            num_estimators=num_estimators,
            early_stopping_rounds=early_stopping_rounds,
            validation_split=validation_split,
            error_threshold=error_threshold,
        )
        return result
    except ValueError as e:
        print(e)
        return None


# Example usage
if __name__ == "__main__":
    # Define the input data and target column
    input_data = Dataset.from_gcs("gs://your-bucket/input-data.csv")
    target_column = "target_column"

    # Define the parameters
    learning_rate = 0.01
    max_depth = 3
    num_estimators = 100
    early_stopping_rounds = 5
    validation_split = 0.2
    error_threshold = 0.8

    # Call the train_until_good_pipeline function
    result = train_until_good_pipeline(
        input_data=input_data,
        target_column=target_column,
        learning_rate=learning_rate,
        max_depth=max_depth,
        num_estimators=num_estimators,
        early_stopping_rounds=early_stopping_rounds,
        validation_split=validation_split,
        error_threshold=error_threshold,
    )

    # Print the result
    if result is not None:
        print(result)
    else:
        print("Failed to train the model.")
