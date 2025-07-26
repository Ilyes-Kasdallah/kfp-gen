
from kfp import pipeline
from kfp.components import load_data

@pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from a remote CSV URL
    data = load_data("https://raw.githubusercontent.com/yourusername/diabetes-prediction/master/data/diabetes.csv")

    # Define the Logistic Regression model
    model = "sklearn.linear_model.LogisticRegression"

    # Define the pipeline function
    return {
        "load_data": data,
        "model": model,
        "predict": "sklearn.linear_model.predict"
    }
