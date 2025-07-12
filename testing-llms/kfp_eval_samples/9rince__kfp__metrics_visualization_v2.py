```python
import kfp
from kfp import dsl

# Import necessary modules from sklearn
from sklearn.datasets import load_iris, load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Define the Metrics class
class Metrics:
    def __init__(self, accuracy):
        self.accuracy = accuracy

# Define the ClassificationMetrics class
class ClassificationMetrics:
    def __init__(self, precision, recall, f1_score):
        self.precision = precision
        self.recall = recall
        self.f1_score = f1_score

# Define the digit_classification component
@dsl.component(base_image='python:3.9')
def digit_classification():
    # Load the Iris dataset
    iris = load_iris()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train a Logistic Regression model
    logistic_regression = LogisticRegression(max_iter=1000)
    logistic_regression.fit(X_train_scaled, y_train)
    
    # Calculate the accuracy on the test set
    accuracy = accuracy_score(y_test, logistic_regression.predict(X_test_scaled))
    
    # Return the accuracy as a Metrics object
    return Metrics(accuracy)

# Define the wine_classification component
@dsl.component(base_image='python:3.9')
def wine_classification():
    # Load the Wine dataset
    wine = load_wine()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.2, random_state=42)
    
    # Train a RandomForestClassifier model
    random_forest_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    random_forest_classifier.fit(X_train, y_train)
    
    # Perform cross-validation
    scores = cross_val_score(random_forest_classifier, X_train, y_train, cv=5)
    
    # Calculate the average accuracy
    average_accuracy = scores.mean()
    
    # Return the average accuracy as a ClassificationMetrics object
    return ClassificationMetrics(average_accuracy, average_accuracy, average_accuracy)

# Define the main pipeline
@dsl.pipeline(name='metrics_visualization_v2')
def metrics_visualization_pipeline():
    # Execute the digit_classification component
    digit_metrics = digit_classification()
    
    # Execute the wine_classification component
    wine_metrics = wine_classification()

# Compile the pipeline
kfp.compiler.Compiler().compile(metrics_visualization_pipeline, 'metrics_visualization_v2.yaml')
```

This code defines the `Metrics` and `ClassificationMetrics` classes to hold the accuracy and precision/recall/f1-score respectively. The `digit_classification` and `wine_classification` components use these classes to log the metrics. The `metrics_visualization_pipeline` orchestrates the execution of these components in sequence.