
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

        # Train the model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")

    # Define the second component: visualization
    @dsl.component(name="visualization")
    def visualization():
        import matplotlib.pyplot as plt

        # Plot the confusion matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap='Blues')
        plt.colorbar()
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')

        # Save the plot
        plt.savefig('confusion_matrix.png')

# Run the pipeline
pipeline = metrics_visualization_v2()
pipeline.run()
