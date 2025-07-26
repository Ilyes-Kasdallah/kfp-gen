import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator


@dsl.pipeline(name="MNIST Pipeline")
def mnist_REST_API_temp():
    # Define the input data generator
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255, validation_split=0.2, batch_size=32, class_mode="binary"
    )

    # Load the MNIST dataset
    (x_train, y_train), (x_test, y_test) = mnist_rest_api_temp.load_data()

    # Create the model
    model = Sequential(
        [
            Flatten(input_shape=(28, 28)),
            Dense(128, activation="relu"),
            Dense(10, activation="softmax"),
        ]
    )

    # Compile the model
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    # Train the model
    model.fit(
        train_datagen.flow(
            x_train, y_train, epochs=10, validation_data=(x_test, y_test)
        )
    )

    # Save the trained model
    model.save("mnist_model.h5")


# Example usage of the pipeline
mnist_REST_API_temp()
