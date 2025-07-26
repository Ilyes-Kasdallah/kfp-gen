
from kfp import dsl

@dsl.pipeline(name="HypertensionPredictionPipeline")
def hypertension_prediction():
    # Load hypertension data from a CSV file
    load_data = dsl.component(
        name="load_data",
        inputs={
            "csv_file": dsl.file_path("https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/hypertension_data.csv")
        },
        outputs={
            "data": dsl.output_type(pandas.DataFrame)
        }
    )

    # Predict hypertension based on the loaded data
    predict_hypertension = dsl.component(
        name="predict_hypertension",
        inputs={
            "data": dsl.input_type(pandas.DataFrame)
        },
        outputs={
            "prediction": dsl.output_type(pandas.Series)
        }
    )

    # Return the prediction
    return predict_hypertension()
