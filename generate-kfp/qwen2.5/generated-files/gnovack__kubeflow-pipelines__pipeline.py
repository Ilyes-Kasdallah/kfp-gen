
from kfp import dsl

@dsl.pipeline(name="Boston Housing Pipeline")
def Boston_Housing_Pipeline():
    # Define the preprocessing step
    preprocess_step = dsl.component(
        name="preprocess_data",
        image="gnovack/boston_pipeline_preprocessing:latest",
        inputs={
            "data": dsl.input("data")
        },
        outputs={
            "x_train": dsl.output("x_train"),
            "x_test": dsl.output("x_test"),
            "y_train": dsl.output("y_train")
        }
    )

    # Define the model training step
    train_step = dsl.component(
        name="train_model",
        image="gnovack/boston_pipeline_training:latest",
        inputs={
            "x_train": dsl.input("x_train"),
            "y_train": dsl.input("y_train")
        },
        outputs={
            "model": dsl.output("model")
        }
    )

    # Define the model evaluation step
    evaluate_step = dsl.component(
        name="evaluate_model",
        image="gnovack/boston_pipeline_evaluation:latest",
        inputs={
            "model": dsl.input("model")
        },
        outputs={
            "accuracy": dsl.output("accuracy")
        }
    )

    # Define the pipeline execution
    pipeline_execution = preprocess_step + train_step + evaluate_step

    return pipeline_execution
