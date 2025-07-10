from kfp import dsl
from kfp.dsl import Input, Output, Dataset, component

@dsl.component(base_image="python:3.9")
def prepare_features(
    raw_dataset: Input[Dataset],
    training_features: Output[Dataset],
    testing_features: Output[Dataset],
    training_labels: Output[Dataset],
    testing_labels: Output[Dataset]
):
    """Transform and split the dataset for modeling."""
    import subprocess
    subprocess.run(["pip", "install", "pandas", "scikit-learn"], check=True)
    
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import train_test_split
    
    dataset = pd.read_csv(raw_dataset.path)
    assert dataset.notna().all().all(), "Dataset contains missing values"
    
    features = dataset.drop(columns=['species_class'])
    target = dataset['species_class']
    
    feature_transformer = RobustScaler()
    normalized_features = feature_transformer.fit_transform(features)
    
    X_train, X_test, y_train, y_test = train_test_split(
        normalized_features, 
        target,
        test_size=0.25,
        random_state=42,
        stratify=target
    )
    
    train_df = pd.DataFrame(X_train, columns=features.columns)
    test_df = pd.DataFrame(X_test, columns=features.columns)
    train_labels_df = pd.DataFrame(y_train, columns=['species_class'])
    test_labels_df = pd.DataFrame(y_test, columns=['species_class'])
    
    train_df.to_csv(training_features.path, index=False)
    test_df.to_csv(testing_features.path, index=False)
    train_labels_df.to_csv(training_labels.path, index=False)
    test_labels_df.to_csv(testing_labels.path, index=False)
