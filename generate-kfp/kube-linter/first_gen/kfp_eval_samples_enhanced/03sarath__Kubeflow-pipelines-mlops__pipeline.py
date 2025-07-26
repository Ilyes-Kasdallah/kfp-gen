import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the download component
@component
def download_data():
    # Load the Iris dataset
    iris = load_iris()
    # Return the dataset as a dictionary
    return {"data": iris.data, "target": iris.target}


# Define the first pipeline
@pipeline(name="First Pipeline")
def first_pipeline():
    # Download the dataset
    dataset = download_data()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        dataset["data"], dataset["target"], test_size=0.2, random_state=42
    )

    # Initialize Decision Tree classifier
    dt_classifier = DecisionTreeClassifier(random_state=42)

    # Train the classifier
    dt_classifier.fit(X_train, y_train)

    # Initialize Logistic Regression classifier
    lr_classifier = LogisticRegression(random_state=42)

    # Train the classifier
    lr_classifier.fit(X_train, y_train)

    # Make predictions
    y_pred_dt = dt_classifier.predict(X_test)
    y_pred_lr = lr_classifier.predict(X_test)

    # Calculate accuracy
    accuracy_dt = accuracy_score(y_test, y_pred_dt)
    accuracy_lr = accuracy_score(y_test, y_pred_lr)

    # Print the results
    print(f"Decision Tree Accuracy: {accuracy_dt}")
    print(f"Logistic Regression Accuracy: {accuracy_lr}")


# Run the pipeline
first_pipeline()
