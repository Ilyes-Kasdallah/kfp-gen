
from kfp import dsl

@dsl.pipeline(name="metrics_visualization_v2")
def metrics_visualization_v2():
    # Define the first component: digit_classification
    @dsl.component(name="digit_classification")
    def digit_classification():
        from sklearn.datasets import load_iris
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score

        # Load the Iris dataset
        iris = load_iris()
        X = iris.data
        y = iris.target

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the logistic regression model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")

# Run the pipeline
pipeline = metrics_visualization_v2()
pipeline.run()
