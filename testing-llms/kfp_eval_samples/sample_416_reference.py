from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Model, component

@dsl.component(base_image="python:3.9")
def assess_performance(
    testing_features: Input[Dataset],
    testing_labels: Input[Dataset],
    trained_model: Input[Model],
    performance_metrics: Output[Dataset]
):
    """Evaluate model performance and generate visualization."""
    import subprocess
    subprocess.run(["pip", "install", "pandas", "scikit-learn", "seaborn", "joblib"], check=True)
    
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.metrics import classification_report, confusion_matrix
    from joblib import load
    
    X_test = pd.read_csv(testing_features.path)
    y_true = pd.read_csv(testing_labels.path)['species_class']
    classifier = load(trained_model.path)
    
    y_pred = classifier.predict(X_test)
    
    metrics = classification_report(y_true, y_pred, output_dict=True)
    conf_matrix = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='YlOrRd')
    plt.title('Confusion Matrix Heatmap')
    plt.xlabel('Predicted Class')
    plt.ylabel('Actual Class')
    
    results = {
        'metrics': metrics,
        'confusion_matrix': conf_matrix.tolist()
    }
    pd.DataFrame([results]).to_json(performance_metrics.path)
