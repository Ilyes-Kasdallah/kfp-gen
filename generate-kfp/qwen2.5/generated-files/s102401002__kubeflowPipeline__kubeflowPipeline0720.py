
from kfp import pipeline
from kfp.components import load_data

@pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from a specified URL
    data = load_data("https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k")

    # Define the logistic regression model
    model = "sklearn.linear_model.LogisticRegression"

    # Define the pipeline steps
    predict_step = model.predict(data)

    return predict_step
