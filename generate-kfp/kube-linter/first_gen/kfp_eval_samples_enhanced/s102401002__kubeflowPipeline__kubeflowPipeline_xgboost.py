import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


# Define the pipeline function
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from URLs
    data1 = load_diabetes()
    data2 = load_diabetes()

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data1.data, data1.target, test_size=0.2, random_state=42
    )

    # Create an XGBoost classifier
    model = XGBClassifier(max_depth=3, learning_rate=0.1, n_estimators=100)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    # Return the accuracy
    return accuracy


# Example usage of the pipeline function
if __name__ == "__main__":
    pipeline.run(diabetes_prediction_pipeline)
