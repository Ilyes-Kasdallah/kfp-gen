import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Boston Housing Pipeline")
def BostonHousingPipeline():
    # Preprocess Data
    x_train = component(
        name="x_train",
        image="gnovack/boston_pipeline_preprocessing:latest",
        inputs={"data": Input(Dataset("boston_housing"))},
        outputs={"x_train": Output(Dataset("x_train.npy"))},
    )

    # Predict Boston Housing Prices
    x_test = component(
        name="x_test",
        image="gnovack/boston_pipeline_predict:latest",
        inputs={
            "x_train": Input(Dataset("x_train.npy")),
            "model": Input(Model("boston_housing_model")),
        },
        outputs={"predictions": Output(Dataset("predictions.npy"))},
    )

    # Return the results
    return x_train, x_test, predictions


# Compile the pipeline
kfp.compiler.Compiler().compile(BostonHousingPipeline)
