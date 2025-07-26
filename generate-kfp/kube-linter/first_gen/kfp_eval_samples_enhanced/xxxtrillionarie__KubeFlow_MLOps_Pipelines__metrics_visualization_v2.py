import kfp
from kfp.dsl import pipeline, component

# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix


# Define the pipeline function
@dsl.pipeline(name="metrics_visualization_v2")
def metrics_visualization_v2():
    # Load the Iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Create a logistic regression model
    model = LogisticRegression()

    # Train the model
    model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Log the metrics
    print(f"Accuracy: {accuracy}")
    print("Confusion Matrix:")
    print(cm)


# Run the pipeline
if __name__ == "__main__":
    metrics_visualization_v2()
