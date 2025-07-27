import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the Iris dataset
@component
def load_iris():
    """Load the Iris dataset."""
    iris = sklearn.datasets.load_iris()
    return iris


# Define the data preparation component
@component
def data_prep(iris):
    """Preprocess the Iris dataset."""
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


# Define the model training component
@component
def train_model(X_train, y_train):
    """Train a simple linear regression model."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


# Define the pipeline
@pipeline(name="11_iris_training_pipeline")
def iris_training_pipeline():
    """Run the Iris training pipeline."""
    X_train, X_test, y_train, y_test = data_prep(load_iris())
    model = train_model(X_train, y_train)
    return model


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(iris_training_pipeline)
