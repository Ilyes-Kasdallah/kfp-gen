from kfp.dsl import component, Output, ClassificationMetrics,Markdown
from typing import NamedTuple, Dict, Any
import io

@component(
    packages_to_install=['pandas', 'scikit-learn', 'minio', 'boto3'],
)
def model_validation_with_serializable_metrics(
    metrics: Output[ClassificationMetrics],
    markdown: Output[Markdown],
    model_path: str,
    test_data_dir: str,
    minio_endpoint: str = 'minio:9000',
    minio_access_key: str = 'minio',
    minio_secret_key: str = 'minio123',
    test_size: float = 0.2,
    random_state: int = 42
) -> NamedTuple('Outputs', [
    ('accuracy', float), 
    ('precision', float), 
    ('recall', float), 
]):
    import pandas as pd
    import joblib
    import boto3
    from io import BytesIO
    from sklearn.metrics import (
        accuracy_score, 
        precision_score, 
        recall_score, 
        classification_report, 
        confusion_matrix
    )
    from sklearn.model_selection import train_test_split
    from collections import namedtuple
    try: 
        # Create S3 client
        s3 = boto3.client(
            's3',
            endpoint_url=f'http://{minio_endpoint}',
            aws_access_key_id=minio_access_key,
            aws_secret_access_key=minio_secret_key,
            config=boto3.session.Config(signature_version='s3v4'),
            verify=False
        )

        # Load data
        data_obj = s3.get_object(Bucket='titanic-data', Key='titanic_data.csv')
        data = pd.read_csv(data_obj['Body'])

        # Load model directly from S3
        model_obj = s3.get_object(Bucket='titanic-model', Key='logistic_model.pkl')
        model_bytes = model_obj['Body'].read()
        model = joblib.load(BytesIO(model_bytes))

        # Prepare features
        feature_columns = [
            'Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 
            'Sex_male', 'Embarked_Q', 'Embarked_S'
        ]
        X = data[feature_columns]
        y = data['Survived']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state
        )

        # Predictions and metrics
        y_pred = model.predict(X_test)
        
        # Compute metrics
        accuracy = float(accuracy_score(y_test, y_pred))
        precision = float(precision_score(y_test, y_pred, average='binary'))
        recall = float(recall_score(y_test, y_pred, average='binary'))
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics.log_confusion_matrix(['Not Survived', 'Survived'], cm.tolist())
        
        # classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # use markdown to display classification report
        markdown_content = f"""
        # Classification Report
        | Class | Precision | Recall | F1-Score | Support | 
        | --- | --- | --- | --- | --- |
        | Not Survived | {report['0']['precision']} | {report['0']['recall']} | {report['0']['f1-score']} | {report['0']['support']} |
        | Survived | {report['1']['precision']} | {report['1']['recall']} | {report['1']['f1-score']} | {report['1']['support']} |  
        """
        with open(markdown.path, 'w') as f:
            f.write(markdown_content)
        
        # Prepare output
        output = namedtuple('Outputs', [
            'accuracy', 'precision', 'recall'
        ])
        return output(
            accuracy, 
            precision, 
            recall, 
        )
    except Exception as e:
        print(f"Validation failed: {e}")
        raise RuntimeError(f"Validation failed: {e}")
    