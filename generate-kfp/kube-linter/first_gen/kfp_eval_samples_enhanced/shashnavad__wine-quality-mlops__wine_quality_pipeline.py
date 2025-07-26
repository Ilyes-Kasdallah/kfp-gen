import kfp
from kfp.dsl import pipeline, component, Input, Output, Dataset, TextIO

# Import necessary libraries
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Define the preprocessing component
@component
def preprocess(data_path: TextIO) -> (Dataset, Dataset, StandardScaler):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(data_path)

    # Split the DataFrame into features and labels
    X = df.drop(columns=["quality"])
    y = df["quality"]

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Save the preprocessed features, labels, and scaler object
    dataset = Dataset.from_pandas(
        X_scaled, schema={"features": "float32", "labels": "int32"}
    )
    labels = Dataset.from_pandas(y, schema={"labels": "int32"})
    scaler.save_to_disk("scaler")

    return dataset, labels, scaler


# Define the wine quality prediction component
@component
def predict_quality(dataset: Dataset, labels: Dataset, scaler: StandardScaler) -> float:
    # Load the preprocessed features, labels, and scaler object
    X = dataset.to_pandas()
    y = labels.to_pandas()
    scaler.load_from_disk("scaler")

    # Make predictions
    predictions = scaler.predict(X)

    # Calculate accuracy
    accuracy = accuracy_score(y, predictions)

    return accuracy


# Define the pipeline
@pipeline(name="wine_quality_pipeline")
def wine_quality_pipeline():
    # Preprocess the data
    dataset, labels, scaler = preprocess("wine_data.csv")

    # Predict the quality
    accuracy = predict_quality(dataset, labels, scaler)

    print(f"Accuracy: {accuracy}")


# Run the pipeline
if __name__ == "__main__":
    pipeline.run()
