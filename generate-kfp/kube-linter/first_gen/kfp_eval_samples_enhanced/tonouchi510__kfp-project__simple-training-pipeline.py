import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten


# Define the training component
@component
def training(
    model_type: str = "resnet",
    epochs: int = 5,
    batch_size: int = 32,
    validation_split: float = 0.2,
) -> keras.Model:
    # Load the dataset
    train_datagen = ImageDataGenerator(rescale=1.0 / 255)
    train_generator = train_datagen.flow_from_directory(
        "path/to/train/directory",
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode="binary",
        validation_split=validation_split,
    )

    # Build the model
    model = Sequential(
        [
            Flatten(input_shape=(224, 224)),
            Dense(64, activation="relu"),
            Dropout(0.2),
            Dense(1, activation="sigmoid"),
        ]
    )

    # Compile the model
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    return model


# Define the pipeline
@pipeline(name="simple-training-pipeline")
def simple_training_pipeline():
    # Train the model
    model = training(model_type="resnet", epochs=5, batch_size=32, validation_split=0.2)

    # Save the model
    model.save("path/to/model.h5")


# Run the pipeline
if __name__ == "__main__":
    simple_training_pipeline()
