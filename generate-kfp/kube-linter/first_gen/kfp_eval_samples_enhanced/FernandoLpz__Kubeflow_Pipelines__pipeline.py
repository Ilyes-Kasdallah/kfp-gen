import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the pipeline function
@dsl.pipeline(name="First Pipeline")
def first_pipeline():
    # Step 1: Download the dataset
    @component
    def download_data():
        # Load the dataset
        data = load_iris()
        # Save the dataset to a file
        data.to_csv("data.csv", index=False)
        return data

    # Step 2: Split the dataset into training and testing sets
    @component
    def split_data(data):
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    # Step 3: Train a Decision Tree model
    @component
    def train_decision_tree(X_train, y_train):
        # Initialize the Decision Tree classifier
        clf = DecisionTreeClassifier(random_state=42)
        # Train the model
        clf.fit(X_train, y_train)
        return clf

    # Step 4: Train a Logistic Regression model
    @component
    def train_logistic_regression(X_train, y_train):
        # Initialize the Logistic Regression classifier
        clf = LogisticRegression(random_state=42)
        # Train the model
        clf.fit(X_train, y_train)
        return clf

    # Step 5: Evaluate the models
    @component
    def evaluate_models(clf, X_test, y_test):
        # Make predictions on the test set
        predictions = clf.predict(X_test)
        # Calculate accuracy
        accuracy = accuracy_score(y_test, predictions)
        return accuracy

    # Main function to run the pipeline
    @dsl.function
    def main():
        # Download the dataset
        data = download_data()
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = split_data(data)
        # Train the Decision Tree model
        clf = train_decision_tree(X_train, y_train)
        # Train the Logistic Regression model
        clf = train_logistic_regression(X_train, y_train)
        # Evaluate the models
        accuracy = evaluate_models(clf, X_test, y_test)
        print(f"Accuracy: {accuracy}")


# Run the pipeline
if __name__ == "__main__":
    main()
