import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="resnet_cifar10_pipeline")
def resnet_cifar10_pipeline():
    # Define the preprocessing step
    preprocess_op = component(
        name="preprocess_op",
        description="Preprocesses the raw data.",
        inputs={
            "raw_data": Input(Dataset("raw_data")),
        },
        outputs={
            "processed_data": Output(Dataset("processed_data")),
        },
        steps=[
            {
                "name": "normalize_data",
                "inputs": {
                    "data": Input(Dataset("raw_data")),
                },
                "outputs": {
                    "normalized_data": Output(Dataset("normalized_data")),
                },
                "code": """
                    import numpy as np

                    def normalize_data(data):
                        return (data - data.min()) / (data.max() - data.min())
                """,
            },
            {
                "name": "resize_data",
                "inputs": {
                    "data": Input(Dataset("processed_data")),
                },
                "outputs": {
                    "resized_data": Output(Dataset("resized_data")),
                },
                "code": """
                    import numpy as np

                    def resize_data(data):
                        return np.resize(data, (32, 32))
                """,
            },
        ],
    )

    # Define the model training step
    model_training_op = component(
        name="model_training_op",
        description="Trains a ResNet model on the CIFAR-10 dataset.",
        inputs={
            "input_data": Input(Dataset("resized_data")),
            "labels": Input(Dataset("labels")),
        },
        outputs={
            "model": Output(Model("model")),
        },
        steps=[
            {
                "name": "train_model",
                "inputs": {
                    "model": Input(Model("model")),
                    "input_data": Input(Dataset("resized_data")),
                    "labels": Input(Dataset("labels")),
                },
                "outputs": {
                    "metrics": Output(Metrics("metrics")),
                },
                "code": """
                    from tensorflow.keras.models import Sequential
                    from tensorflow.keras.layers import Dense, Flatten

                    model = Sequential([
                        Flatten(input_shape=(32, 32)),
                        Dense(64, activation='relu'),
                        Dense(128, activation='relu'),
                        Dense(10, activation='softmax')
                    ])
                    model.compile(optimizer='adam',
                                loss='sparse_categorical_crossentropy',
                                metrics=['accuracy'])
                """,
            },
        ],
    )

    # Define the serving step
    serving_op = component(
        name="serving_op",
        description="Serves the trained ResNet model.",
        inputs={
            "model": Input(Model("model")),
        },
        outputs={
            "output": Output(Dataset("output")),
        },
        steps=[
            {
                "name": "predict_output",
                "inputs": {
                    "model": Input(Model("model")),
                    "input_data": Input(Dataset("output")),
                },
                "outputs": {
                    "predictions": Output(Dataset("predictions")),
                },
                "code": """
                    import numpy as np

                    def predict_output(model, input_data):
                        predictions = model.predict(input_data)
                        return predictions
                """,
            },
        ],
    )

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Return the pipeline function
    return pipeline(
        pipeline_root=pipeline_root,
        preprocess_op=preprocess_op,
        model_training_op=model_training_op,
        serving_op=serving_op,
    )
