
from kfp import dsl

@dsl.pipeline(name="End2end Resnet50 Classification")
def end2end_resnet50_classification(raw_data_dir, processed_data_dir):
    # Define the preprocessing step
    preprocess = dsl.component(
        name="Preprocess",
        description="Preprocesses raw image data",
        inputs={
            "raw_data_dir": dsl.input("raw_data_dir"),
            "processed_data_dir": dsl.output("processed_data_dir")
        },
        outputs={
            "processed_image": dsl.output("processed_image")
        },
        steps=[
            dsl.task(
                name="Load Image",
                description="Loads an image from the input directory",
                inputs={
                    "raw_data_dir": dsl.input("raw_data_dir")
                },
                outputs={
                    "image": dsl.output("image")
                }
            ),
            dsl.task(
                name="Resize Image",
                description="Resizes the image to a fixed size",
                inputs={
                    "image": dsl.input("image"),
                    "output_size": dsl.input("output_size")
                },
                outputs={
                    "resized_image": dsl.output("resized_image")
                }
            ),
            dsl.task(
                name="Normalize Image",
                description="Normalizes the image to have a mean of 0 and a standard deviation of 1",
                inputs={
                    "resized_image": dsl.input("resized_image")
                },
                outputs={
                    "normalized_image": dsl.output("normalized_image")
                }
            ),
            dsl.task(
                name="Convert to Tensor",
                description="Converts the image to a tensor",
                inputs={
                    "normalized_image": dsl.input("normalized_image")
                },
                outputs={
                    "tensor": dsl.output("tensor")
                }
            ),
            dsl.task(
                name="Reshape Tensor",
                description="Reshapes the tensor to match the ResNet50 input format",
                inputs={
                    "tensor": dsl.input("tensor"),
                    "input_shape": dsl.input("input_shape")
                },
                outputs={
                    "reshaped_tensor": dsl.output("reshaped_tensor")
                }
            ),
            dsl.task(
                name="Model Prediction",
                description="Makes predictions on the reshaped tensor",
                inputs={
                    "reshaped_tensor": dsl.input("reshaped_tensor")
                },
                outputs={
                    "predictions": dsl.output("predictions")
                }
            )
        ]
    )

    # Define the serving step
    serve = dsl.component(
        name="Serve",
        description="Serves the model for inference",
        inputs={
            "model": dsl.input("model"),
            "input_shape": dsl.input("input_shape")
        },
        outputs={
            "predictions": dsl.output("predictions")
        },
        steps=[
            dsl.task(
                name="Predictions",
                description="Makes predictions on the input data",
                inputs={
                    "model": dsl.input("model"),
                    "input_shape": dsl.input("input_shape")
                },
                outputs={
                    "predictions": dsl.output("predictions")
                }
            )
        ]
    )

    # Combine the preprocessing and serving steps into a single pipeline
    return preprocess + serve

# Example usage
raw_data_dir = "/path/to/raw/data"
processed_data_dir = "/path/to/processed/data"

pipeline = end2end_resnet50_classification(raw_data_dir, processed_data_dir)
