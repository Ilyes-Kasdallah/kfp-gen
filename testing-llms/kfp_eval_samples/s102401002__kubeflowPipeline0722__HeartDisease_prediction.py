```python
import kfp
from kfp import dsl

# Load data component
@dsl.component(
    base_image='python:3.9',
    packages_to_install=['pandas==2.2.2'],
    outputs=[dsl.Output('data_output', artifact_class=dsl.Artifact)]
)
def load_data():
    # Load data from URL
    import pandas as pd
    url = 'https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/heart_2020_cleaned.csv'
    df = pd.read_csv(url)

    # Drop unnecessary columns
    df.drop(columns=['PhysicalHealth', 'MentalHealth', 'Race', 'GenHealth'], inplace=True)

    # Map categorical features to numerical representations
    mapping = {
        'HeartDisease': {'No': 0, 'Yes': 1},
        'Smoking': {'No': 0, 'Yes': 1},
        'AlcoholDrinking': {'None': 0, 'Light': 1, 'Moderate': 2, 'Heavy': 3},
        'Stroke': {'No': 0, 'Yes': 1},
        'DiffWalking': {'No': 0, 'Very Hard': 1},
        'Sex': {'Male': 0, 'Female': 1},
        'AgeCategory': {f'0-{str(i)}': i for i in range(1, 8)},
        'Diabetic': {'No': 0, 'Yes': 1},
        'PhysicalActivity': {'Never': 0, 'Seldom': 1, 'Occasionally': 2, 'Regularly': 3},
        'Asthma': {'No': 0, 'Yes': 1},
        'KidneyDisease': {'No': 0, 'Yes': 1},
        'SkinCancer': {'No': 0, 'Yes': 1}
    }
    df.replace(mapping, inplace=True)

    return df

# Train model component
@dsl.component(
    base_image='python:3.9',
    packages_to_install=['scikit-learn']
)
def train_model(data_input):
    # Assuming scikit-learn is used for training
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression

    # Load data
    df = data_input.get()

    # Split data into features and target
    X = df.drop('HeartDisease', axis=1)
    y = df['HeartDisease']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and fit the model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    return model

# Evaluate model component
@dsl.component(
    base_image='python:3.9',
    packages_to_install=['scikit-learn']
)
def evaluate_model(model_input, data_input):
    # Assuming scikit-learn is used for evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    # Load model
    model = model_input.get()

    # Load data
    df = data_input.get()

    # Split data into features and target
    X = df.drop('HeartDisease', axis=1)
    y = df['HeartDisease']

    # Predict on test set
    y_pred = model.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary')
    f1 = f1_score(y_test, y_pred, average='binary')

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# HeartDiseasePrediction pipeline
@dsl.pipeline(name='HeartDiseasePrediction')
def heart_disease_prediction():
    # Load data
    load_data_task = load_data()

    # Train model
    train_model_task = train_model(load_data_task.outputs['data_output'])

    # Evaluate model
    evaluate_model_task = evaluate_model(train_model_task.outputs['model'], load_data_task.outputs['data_output'])
```

This code defines a Kubeflow Pipeline named `HeartDiseasePrediction` with three components: `load_data`, `train_model`, and `evaluate_model`. Each component is defined using the `@dsl.component` decorator, specifying the base image, required packages, and outputs. The pipeline's control flow is sequential, with each component depending on the previous one. The pipeline uses the Kubeflow Pipelines DSL library (`kfp.dsl`).