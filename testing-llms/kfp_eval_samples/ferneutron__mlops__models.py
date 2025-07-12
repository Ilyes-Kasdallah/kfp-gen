```python
import kfp
from kfp import dsl
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

# Define the decision tree component
@dsl.component(
    base_image="gcr.io/deeplearning-platform-release/tf2-cpu.2-6:latest",
    packages_to_install=["pandas==1.3.5", "joblib==1.1.0"],
)
def decision_tree(train_dataset: dsl.Input[ds.Dataset]) -> dsl.Output[dsl.Artifact]:
    # Load the iris dataset
    iris = load_iris()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
    
    # Train a DecisionTreeClassifier model
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = clf.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Create a DataFrame to store the metrics
    metrics_df = pd.DataFrame({
        'metric': ['accuracy'],
        'value': [accuracy]
    })
    
    # Serialize the model
    joblib.dump(clf, 'model.joblib')
    
    # Return the metrics and the serialized model
    return dsl.Output(metrics=metrics_df), dsl.Output(output_model='model.joblib')

# Define the random forest component
@dsl.component(
    base_image="gcr.io/deeplearning-platform-release/tf2-cpu.2-6:latest",
    packages_to_install=["pandas==1.3.5", "joblib==1.1.0"],
)
def random_forest(train_dataset: dsl.Input[ds.Dataset]) -> dsl.Output[dsl.Artifact]:
    # Load the iris dataset
    iris = load_iris()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
    
    # Train a RandomForestClassifier model
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = clf.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Create a DataFrame to store the metrics
    metrics_df = pd.DataFrame({
        'metric': ['accuracy'],
        'value': [accuracy]
    })
    
    # Serialize the model
    joblib.dump(clf, 'model.joblib')
    
    # Return the metrics and the serialized model
    return dsl.Output(metrics=metrics_df), dsl.Output(output_model='model.joblib')

# Define the main pipeline
@dsl.pipeline(name="IrisClassificationPipeline")
def iris_classification_pipeline():
    # Input dataset
    train_dataset = dsl.Input[ds.Dataset]()
    
    # Decision tree component
    decision_tree_output = decision_tree(train_dataset=train_dataset)
    
    # Random forest component
    random_forest_output = random_forest(train_dataset=train_dataset)

# Compile and run the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(iris_classification_pipeline, "models.yaml")
    kfp.Client().create_run_from_pipeline_package("models.yaml", arguments={"train_dataset": "path/to/iris.csv"})
```

This solution defines a Kubeflow Pipeline named `IrisClassificationPipeline` that includes two components: `decision_tree` and `random_forest`. Each component trains a respective classifier on the Iris dataset and returns model metrics and the trained model. The pipeline is compiled and executed using the Kubeflow Pipelines SDK.