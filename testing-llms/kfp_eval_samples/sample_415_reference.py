from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Model, component

@dsl.component(base_image="python:3.9")
def develop_model(
    training_features: Input[Dataset],
    training_labels: Input[Dataset],
    model_artifact: Output[Model]
):
    """Build and train the classification model."""
    import subprocess
    subprocess.run(["pip", "install", "pandas", "scikit-learn", "joblib"], check=True)
    
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from joblib import dump
    
    X = pd.read_csv(training_features.path)
    y = pd.read_csv(training_labels.path)['species_class']
    
    classifier = LogisticRegression(
        class_weight='balanced',
        max_iter=1000,
        random_state=42,
        multi_class='multinomial'
    )
    classifier.fit(X, y)
    
    dump(classifier, model_artifact.path)