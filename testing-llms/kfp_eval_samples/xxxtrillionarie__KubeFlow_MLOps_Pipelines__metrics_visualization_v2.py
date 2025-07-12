```python
import kfp
from kfp import dsl
from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# Define the Metrics class
class Metrics:
    def __init__(self, accuracy):
        self.accuracy = accuracy

# Define the ClassificationMetrics class
class ClassificationMetrics:
    def __init__(self, roc_auc):
        self.roc_auc = roc_auc

# Define the digit_classification component
@dsl.component(base_image='python:3.9')
def digit_classification():
    # Load the Iris dataset
    iris = load_iris()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.33, random_state=42)
    
    # Create a Logistic Regression model
    model = LogisticRegression(max_iter=1000)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Perform 10-fold cross-validation
    scores = cross_val_score(model, X_train, y_train, cv=10)
    
    # Calculate the final accuracy on the test set
    accuracy = accuracy_score(y_test, model.predict(X_test))
    
    # Return the accuracy as a Metrics object
    return Metrics(accuracy)

# Define the wine_classification component
@dsl.component(base_image='python:3.9')
def wine_classification():
    # Load the Wine dataset
    wine = load_wine()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.33, random_state=42)
    
    # Create a RandomForestClassifier model
    model = RandomForestClassifier(n_estimators=100)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Perform 3-fold cross-validation
    scores = cross_val_score(model, X_train, y_train, cv=3)
    
    # Calculate the classification metrics (ROC AUC)
    roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    
    # Return the classification metrics as a ClassificationMetrics object
    return ClassificationMetrics(roc_auc)

# Define the main pipeline
@dsl.pipeline(name='metrics_visualization_v2')
def metrics_visualization_pipeline():
    # Execute the digit_classification component
    digit_metrics = digit_classification()
    
    # Execute the wine_classification component
    wine_metrics = wine_classification()

# Compile and run the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(metrics_visualization_pipeline, 'metrics_visualization_v2.yaml')
    kfp.Client().create_run_from_pipeline_package('metrics_visualization_v2.yaml', arguments={})
```

This code defines the required components (`digit_classification` and `wine_classification`) and the main pipeline `metrics_visualization_pipeline`. The pipeline executes both components sequentially and returns the results as `Metrics` objects. The pipeline is compiled and executed using the Kubeflow Pipelines SDK.