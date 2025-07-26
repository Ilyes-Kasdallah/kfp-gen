import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the pipeline function
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load the diabetes dataset
    @component
    def load_data():
        data = load_diabetes()
        X = data.data
        y = data.target
        return X, y

    # Split the data into training and testing sets
    @component
    def split_data(X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    # Train a logistic regression model
    @component
    def train_model(X_train, y_train):
        model = LogisticRegression()
        model.fit(X_train, y_train)
        return model

    # Make predictions on the test set
    @component
    def predict_model(model, X_test):
        predictions = model.predict(X_test)
        return predictions

    # Evaluate the model's performance
    @component
    def evaluate_model(predictions, y_test):
        accuracy = accuracy_score(y_test, predictions)
        return accuracy


# Define the pipeline execution
@dsl.pipeline_execution
def execute_pipeline():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)
    predictions = predict_model(model, X_test)
    accuracy = evaluate_model(predictions, y_test)
    print(f"Accuracy: {accuracy}")


# Execute the pipeline
execute_pipeline()
