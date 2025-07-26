import kfp
from kfp.dsl import pipeline, component, Input, Output, Dataset

# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# Define the IrisClassificationPipeline
@dsl.pipeline(name="IrisClassificationPipeline")
def iris_classification_pipeline(train_dataset: Dataset) -> Output[Model]:
    # Load the Iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # Train a DecisionTreeClassifier model
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = accuracy_score(y_test, model.predict(X_test))

    # Return the trained model
    return model
