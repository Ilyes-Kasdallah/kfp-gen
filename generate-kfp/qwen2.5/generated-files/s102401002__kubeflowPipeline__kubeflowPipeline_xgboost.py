
from kfp import pipeline
from kfp.components import load_data, xgboost

@pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from two URLs
    data1 = load_data("https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv")
    data2 = load_data("https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv")

    # Train an XGBoost model on the data
    model = xgboost.train(
        input_data=data1,
        label=data2,
        num_rounds=100,
        objective='binary:logistic',
        eval_metric='accuracy'
    )

    return model

# Example usage
model = diabetes_prediction_pipeline()
print(model)
