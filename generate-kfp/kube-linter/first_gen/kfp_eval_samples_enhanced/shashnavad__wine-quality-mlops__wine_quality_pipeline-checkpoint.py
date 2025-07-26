import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


# Define the download_data component
@component
def download_data():
    # Load the dataset
    data = load_wine()
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )
    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, y_train, X_test_scaled, y_test


# Define the wine_quality_pipeline component
@pipeline(name="wine_quality_pipeline")
def wine_quality_pipeline(
    X_train_scaled: list, y_train: list, X_test_scaled: list, y_test: list
):
    # Define the model
    model = load_wine()

    # Train the model
    model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Return the accuracy
    return accuracy


# Define the wine_quality_pipeline-checkpoint function
@pipeline(name="wine_quality_pipeline-checkpoint")
def wine_quality_pipeline_checkpoint(
    X_train_scaled: list, y_train: list, X_test_scaled: list, y_test: list
):
    # Save the model
    model.save("wine_quality_model.h5")

    # Return the checkpoint
    return "wine_quality_model.h5"
