
from kfp import dsl

@dsl.pipeline(name="resnet_cifar10_pipeline")
def resnet_cifar10_pipeline():
    # Define the preprocessing component
    preprocess_op = dsl.component(
        name="preprocess",
        description="Preprocesses the raw data for the ResNet model.",
        inputs={
            "raw_data": dsl.input(type="string"),
        },
        outputs={
            "processed_data": dsl.output(type="string"),
        },
        steps=[
            dsl.task(
                name="load_data",
                description="Loads the CIFAR-10 dataset.",
                inputs={
                    "data_dir": dsl.input(type="string"),
                },
                outputs={
                    "data": dsl.output(type="string"),
                },
            ),
            dsl.task(
                name="normalize_data",
                description="Normalizes the pixel values in the dataset.",
                inputs={
                    "data": dsl.input(type="string"),
                },
                outputs={
                    "normalized_data": dsl.output(type="string"),
                },
            ),
            dsl.task(
                name="resize_data",
                description="Resizes the images to a fixed size.",
                inputs={
                    "data": dsl.input(type="string"),
                    "size": dsl.input(type="int"),
                },
                outputs={
                    "resized_data": dsl.output(type="string"),
                },
            ),
            dsl.task(
                name="convert_to_tensor",
                description="Converts the image data into a tensor.",
                inputs={
                    "data": dsl.input(type="string"),
                },
                outputs={
                    "tensor": dsl.output(type="tf.Tensor"),
                },
            ),
            dsl.task(
                name="reshape_tensor",
                description="Reshapes the tensor to match the ResNet model's input shape.",
                inputs={
                    "tensor": dsl.input(type="tf.Tensor"),
                },
                outputs={
                    "reshaped_tensor": dsl.output(type="tf.Tensor"),
                },
            ),
            dsl.task(
                name="model_training",
                description="Trains the ResNet model.",
                inputs={
                    "input": dsl.input(type="tf.Tensor"),
                    "labels": dsl.input(type="tf.Tensor"),
                },
                outputs={
                    "model": dsl.output(type="tf.keras.Model"),
                },
            ),
            dsl.task(
                name="evaluate_model",
                description="Evaluates the trained model on the test set.",
                inputs={
                    "model": dsl.input(type="tf.keras.Model"),
                    "test_set": dsl.input(type="tf.data.Dataset"),
                },
                outputs={
                    "accuracy": dsl.output(type="float"),
                },
            ),
            dsl.task(
                name="save_model",
                description="Saves the trained model to a file.",
                inputs={
                    "model": dsl.input(type="tf.keras.Model"),
                    "path": dsl.input(type="string"),
                },
            ),
        ],
    )

    # Define the serving component
    serve_op = dsl.component(
        name="serve",
        description="Serves the trained model on the CIFAR-10 dataset.",
        inputs={
            "model": dsl.input(type="tf.keras.Model"),
            "test_set": dsl.input(type="tf.data.Dataset"),
        },
        outputs={
            "predictions": dsl.output(type="tf.Tensor"),
        },
    )

    # Connect the preprocessing and model training tasks
    preprocess_op.outputs["processed_data"] >> model_training.inputs["input"]
    model_training.outputs["model"] >> serve_op.inputs["model"]

    # Connect the serving and evaluation tasks
    serve_op.outputs["predictions"] >> evaluate_model.inputs["test_set"]
    evaluate_model.outputs["accuracy"] >> serve_op.outputs["accuracy"]

    # Connect the evaluation and saving tasks
    evaluate_model.outputs["accuracy"] >> save_model.inputs["predictions"]
    save_model.outputs["path"] >> serve_op.inputs["path"]

# Run the pipeline
resnet_cifar10_pipeline()
