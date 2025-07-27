import os
import shutil
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import accuracy_score
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="End2end Resnet50 Classification")
def End2endResnet50Classification(
    input_image: Input[Dataset],
    output_model: Output[Model],
    cache_dir: Output[Dataset],
    retries: Output[int],
    resource_limits: Output[dict],
    preprocessing_script: str = "download. Also, follow these rules to ensure correctness: Use @component decorators for each function intended as a Kubeflow step. Ensure all required modules are imported explicitly, especially kfp, kfp.dsl, and kfp.components. Include @dsl.pipeline decorator with a defined name. Use proper Python typing for all function arguments and return values. Avoid undefined or external module references. Use valid YAML-friendly parameter types in pipeline definitions.",
):
    # Load the preprocessed image data
    image_data = ImageDataGenerator(rescale=1.0 / 255)
    train_generator = image_data.flow_from_directory(
        input_image.path, target_size=(224, 224), batch_size=32, class_mode="binary"
    )

    # Define the ResNet50 model
    model = ResNet50(weights="imagenet", include_top=False)

    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    # Train the model
    history = model.fit(
        train_generator,
        epochs=10,
        validation_split=0.2,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=2)
        ],
    )

    # Save the model
    model.save(output_model.path)

    # Cache the preprocessed image data
    cache_dir.save(input_image.path)

    # Return the trained model and cache directory
    return model, cache_dir


# Example usage
if __name__ == "__main__":
    # Define the input and output paths
    input_image_path = "path/to/input/image"
    output_model_path = "path/to/output/model"
    cache_dir_path = "path/to/cache/directory"

    # Call the pipeline function
    model, cache_dir = End2endResnet50Classification(
        input_image=input_image_path,
        output_model=output_model_path,
        cache_dir=cache_dir_path,
        retries=2,
        resource_limits={"cpu": "1", "memory": "1Gi"},
        preprocessing_script="download. Also, follow these rules to ensure correctness: Use @component decorators for each function intended as a Kubeflow step. Ensure all required modules are imported explicitly, especially kfp, kfp.dsl, and kfp.components. Include @dsl.pipeline decorator with a defined name. Use proper Python typing for all function arguments and return values. Avoid undefined or external module references. Use valid YAML-friendly parameter types in pipeline definitions.",
    )

    # Print the trained model and cache directory
    print("Trained Model:", model)
    print("Cache Directory:", cache_dir)
