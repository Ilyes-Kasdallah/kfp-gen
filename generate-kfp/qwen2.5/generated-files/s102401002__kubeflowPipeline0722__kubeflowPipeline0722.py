
from kfp import dsl

@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from two CSV files
    load_data = dsl.component(
        name="load_data",
        description="Load data from two CSV files",
        inputs={
            "url1": "https://raw.githubusercontent.com/yourusername/diabetes-prediction/master/data1.csv",
            "url2": "https://raw.githubusercontent.com/yourusername/diabetes-prediction/master/data2.csv"
        },
        outputs={
            "data": "loaded_data"
        }
    )

    # Predict diabetes
    predict_diabetes = dsl.component(
        name="predict_diabetes",
        description="Predict diabetes",
        inputs={
            "data": "loaded_data"
        },
        outputs={
            "prediction": "predicted_diabetes"
        }
    )

    return load_data, predict_diabetes
