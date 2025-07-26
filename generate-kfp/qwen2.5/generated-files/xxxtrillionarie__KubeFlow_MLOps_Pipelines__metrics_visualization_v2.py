
from kfp import dsl

@dsl.pipeline(name="metrics_visualization_v2")
def metrics_visualization_v2():
    # Define the first component: digit_classification
    @dsl.component(name="digit_classification")
    def digit_classification(data):
        from sklearn.datasets import load_iris
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score

        # Load the Iris dataset
        iris = load_iris()
        X = iris.data
        y = iris.target

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train the logistic regression model
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train_scaled, y_train)

        # Make predictions
        y_pred = model.predict(X_test_scaled)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)

        return accuracy

    # Define the second component: metrics_logging
    @dsl.component(name="metrics_logging")
    def metrics_logging(accuracy):
        print(f"Accuracy: {accuracy}")

# Run the pipeline
pipeline = metrics_visualization_v2()
pipeline.run()
