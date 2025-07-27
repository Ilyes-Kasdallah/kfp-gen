import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from two URLs
    load_data = component(
        name="load_data",
        description="Downloads data from two specified URLs",
        inputs={
            "url1": Input(
                Dataset(
                    "https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv"
                )
            ),
            "url2": Input(
                Dataset(
                    "https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv"
                )
            ),
        },
        outputs={"data": Output(Dataset("diabetes_data.csv"))},
    )

    # Predict diabetes using XGBoost
    predict_diabetes = component(
        name="predict_diabetes",
        description="Predicts diabetes using XGBoost",
        inputs={"data": Input(Dataset("diabetes_data.csv"))},
        outputs={"model": Output(Model("diabetes_model"))},
    )

    # Return the model
    return predict_diabetes


# Compile the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
compiler = kfp.compiler.Compiler()
compiler.compile(diabetes_prediction_pipeline, pipeline_root)
