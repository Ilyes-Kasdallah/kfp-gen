import kfp
from kfp.dsl import pipeline, component, Input, Output

# Import necessary modules
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Define the utils function
@component
def utils():
    # Load the Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train a Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Return the trained model
    return clf


# Define the upload_model function
@component
def upload_model(model_path: Input[str]) -> Output[RandomForestClassifier]:
    # Upload the model to Vertex AI
    from google.cloud import storage
    from google.cloud import aiplatform
    from google.cloud.aiplatform import models

    # Initialize the Vertex AI client
    client = aiplatform.Client()

    # Create a model object
    model = models.Model(
        display_name="iris-model",
        description="A simple Iris model",
        source=model_path,
        version="v1",
        labels={"version": "1.0"},
    )

    # Upload the model to Vertex AI
    client.models.create(model=model)

    # Return the uploaded model
    return model


# Define the pipeline
@pipeline(name="iris_model_upload")
def iris_model_upload():
    # Upload the model
    model = upload_model("path/to/your/model.pkl")

    # Use the model for predictions
    predictions = model.predict([[3, 5, 4]])

    # Print the predictions
    print(predictions)


# Run the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().run(pipeline=iris_model_upload)
