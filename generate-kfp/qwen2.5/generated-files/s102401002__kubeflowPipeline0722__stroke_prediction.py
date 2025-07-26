
from kfp import dsl

@dsl.pipeline(name="Stroke Prediction Pipeline")
def stroke_prediction():
    # Load data from two CSV files
    load_data = dsl.component(
        name="load_data",
        description="Load stroke prediction data from two CSV files",
        inputs={
            "file1": dsl.file("https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/stroke.csv"),
            "file2": dsl.file("https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/stroke.csv")
        },
        outputs={
            "data": dsl.output("data")
        }
    )

    # Perform machine learning model prediction
    predict_stroke = dsl.component(
        name="predict_stroke",
        description="Perform machine learning model prediction on the loaded data",
        inputs={
            "data": dsl.input("data")
        },
        outputs={
            "prediction": dsl.output("prediction")
        }
    )

    # Return the prediction
    return predict_stroke
