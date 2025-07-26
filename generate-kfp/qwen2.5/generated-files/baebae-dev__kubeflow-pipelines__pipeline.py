
from kfp import pipeline
from kfp.components import component

@dsl.pipeline(name="Boston Housing Pipeline")
def Boston_Housing_Pipeline():
    # Preprocess Data Component
    preprocess_data = component(
        name="preprocess_data",
        image="gnovack/boston_pipeline_preprocessing:latest",
        inputs={
            "data": {
                "type": "gcs://path/to/boston_housing.csv"
            }
        },
        outputs={
            "x_train": {
                "type": "numpy.ndarray"
            },
            "x_test": {
                "type": "numpy.ndarray"
            }
        }
    )

    # Model Training Component
    train_model = component(
        name="train_model",
        image="gnovack/boston_pipeline_training:latest",
        inputs={
            "x_train": {
                "type": "numpy.ndarray"
            },
            "x_test": {
                "type": "numpy.ndarray"
            }
        },
        outputs={
            "model": {
                "type": "tf.keras.Model"
            }
        }
    )

    # Model Evaluation Component
    evaluate_model = component(
        name="evaluate_model",
        image="gnovack/boston_pipeline_evaluation:latest",
        inputs={
            "model": {
                "type": "tf.keras.Model"
            },
            "x_test": {
                "type": "numpy.ndarray"
            }
        },
        outputs={
            "accuracy": {
                "type": "float"
            }
        }
    )

    # Main Pipeline
    main_pipeline = pipeline(
        name="Boston Housing Pipeline",
        steps=[
            preprocess_data,
            train_model,
            evaluate_model
        ]
    )
