import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten


# Define the preprocessing component
@component
def preprocess_image(raw_data_dir: str, processed_data_dir: str):
    # Load images from the raw data directory
    image_generator = ImageDataGenerator(rescale=1.0 / 255)
    images = image_generator.flow_from_directory(raw_data_dir, target_size=(224, 224))

    # Save the processed images to the processed data directory
    images.save_to_directory(processed_data_dir)


# Define the end-to-end classification component
@component
def end2end_classification(processed_data_dir: str, model_name: str):
    # Load the preprocessed images
    images = ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        processed_data_dir, target_size=(224, 224)
    )

    # Build the ResNet50 model
    model = Sequential(
        [
            Flatten(input_shape=(224, 224)),
            Dense(64, activation="relu"),
            Dense(10, activation="softmax"),
        ]
    )

    # Compile the model
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    # Train the model
    model.fit(images, epochs=10, validation_split=0.2)


# Define the pipeline
@pipeline(name="End2end Resnet50 Classification")
def end2end_resnet50_classification(
    raw_data_dir: str, processed_data_dir: str, model_name: str
):
    preprocess_image(raw_data_dir, processed_data_dir)
    end2end_classification(processed_data_dir, model_name)


# Run the pipeline
if __name__ == "__main__":
    end2end_resnet50_classification.run()
