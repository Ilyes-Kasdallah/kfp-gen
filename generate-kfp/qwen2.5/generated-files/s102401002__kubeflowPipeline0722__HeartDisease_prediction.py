
from kfp import dsl

@dsl.pipeline(name="HeartDiseasePrediction")
def HeartDiseasePrediction():
    # Load data from a CSV file
    load_data = dsl.component(
        name="load_data",
        inputs={
            "url": "https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/heart_2020_cleaned"
        },
        outputs={
            "data": "loaded_data"
        }
    )

    # Predict heart disease based on the loaded data
    predict_heart_disease = dsl.component(
        name="predict_heart_disease",
        inputs={
            "data": "loaded_data"
        },
        outputs={
            "prediction": "predicted_heart_disease"
        }
    )

    return {
        "load_data": load_data,
        "predict_heart_disease": predict_heart_disease
    }
