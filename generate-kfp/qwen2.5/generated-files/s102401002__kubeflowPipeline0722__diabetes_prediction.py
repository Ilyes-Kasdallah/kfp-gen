
from kfp import dsl

@dsl.pipeline(name="diabetes_prediction")
def diabetes_prediction():
    # Load data from CSV files
    load_data = dsl.component(
        name="load_data",
        description="Load data from CSV files",
        inputs={
            "url1": dsl.uri("https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv"),
            "url2": dsl.uri("https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv")
        },
        outputs={
            "data": dsl.output_type(dsl.Dataset)
        }
    )

    # Predict diabetes using a machine learning model
    predict_diabetes = dsl.component(
        name="predict_diabetes",
        description="Predict diabetes using a machine learning model",
        inputs={
            "data": dsl.input_type(dsl.Dataset)
        },
        outputs={
            "prediction": dsl.output_type(dsl.Tensor)
        }
    )

    # Combine the two components into a single pipeline
    return load_data >> predict_diabetes
