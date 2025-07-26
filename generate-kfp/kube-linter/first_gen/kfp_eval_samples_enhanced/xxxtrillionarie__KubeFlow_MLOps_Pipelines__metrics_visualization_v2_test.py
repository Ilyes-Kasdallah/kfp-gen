import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler


# Define the Wine Classification component
@component
def wine_classification():
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

    # Train the model
    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Return the metrics artifact
    return {"accuracy": accuracy, "confusion_matrix": confusion_matrix(y_test, y_pred)}


# Define the Metrics Visualization Pipeline
@pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_v2_test():
    # Call the Wine Classification component
    result = wine_classification()

    # Print the results
    print("Accuracy:", result["accuracy"])
    print("Confusion Matrix:\n", result["confusion_matrix"])


# Run the pipeline
if __name__ == "__main__":
    metrics_visualization_v2_test()
