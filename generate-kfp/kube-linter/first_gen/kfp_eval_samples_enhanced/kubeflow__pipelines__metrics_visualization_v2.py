import kfp
from kfp.dsl import pipeline, component

# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the digit_classification component
@component
def digit_classification(data):
    # Load the Iris dataset
    iris = load_iris()

    # Split the data into features and target
    X = iris.data
    y = iris.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train the Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    return accuracy


# Define the metrics_visualization_v2 pipeline
@pipeline(name="metrics_visualization_v2")
def metrics_visualization_v2():
    # Call the digit_classification component
    accuracy = digit_classification("data")

    # Print the accuracy
    print(f"Accuracy: {accuracy}")


# Run the pipeline
if __name__ == "__main__":
    metrics_visualization_v2()
