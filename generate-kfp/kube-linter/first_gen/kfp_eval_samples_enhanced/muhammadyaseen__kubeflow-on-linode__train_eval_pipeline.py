import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the pipeline function
@pipeline(name="train_eval_pipeline")
def train_eval_pipeline():
    # Define the training baseline model
    @component
    def train_baseline_model(data):
        # Split data into features and target
        X, y = data["data"], data["target"]

        # Train a logistic regression model
        model = LogisticRegression()
        model.fit(X, y)

        # Return the trained model
        return model

    # Define the evaluation pipeline
    @component
    def evaluate_model(model, test_data):
        # Predict on test data
        predictions = model.predict(test_data)

        # Calculate accuracy
        accuracy = accuracy_score(y, predictions)

        # Return the accuracy
        return accuracy


# Example usage of the pipeline
if __name__ == "__main__":
    # Load the Iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # Train the baseline model
    baseline_model = train_baseline_model(X_train)

    # Evaluate the baseline model
    baseline_accuracy = evaluate_model(baseline_model, X_test)

    print(f"Baseline Model Accuracy: {baseline_accuracy}")
