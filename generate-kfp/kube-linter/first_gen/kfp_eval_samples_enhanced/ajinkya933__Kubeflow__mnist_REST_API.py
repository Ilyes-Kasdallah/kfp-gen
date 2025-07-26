import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint


@dsl.pipeline(name="MNIST Pipeline")
def mnist_training_pipeline():
    # Step 1: Load and preprocess the dataset
    @component
    def load_and_preprocess_data():
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_train = x_train.astype("float32") / 255.0
        x_test = x_test.astype("float32") / 255.0
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        return x_train, y_train, x_test, y_test

    # Step 2: Build the model
    @component
    def build_model():
        model = Sequential(
            [
                Flatten(input_shape=(28, 28)),
                Dense(128, activation="relu"),
                Dense(10, activation="softmax"),
            ]
        )
        model.compile(
            optimizer=Adam(), loss="categorical_crossentropy", metrics=["accuracy"]
        )
        return model

    # Step 3: Train the model
    @component
    def train_model(model):
        checkpoint = ModelCheckpoint(
            "mnist_model.h5", save_best_only=True, monitor="val_accuracy"
        )
        model.fit(x_train, y_train, epochs=10, batch_size=32, callbacks=[checkpoint])
        return model

    # Step 4: Evaluate the model
    @component
    def evaluate_model(model):
        test_loss, test_acc = model.evaluate(x_test, y_test)
        return test_loss, test_acc

    # Step 5: Save the trained model
    @component
    def save_model(model):
        model.save("mnist_model.h5")

    # Step 6: Run the pipeline
    @component
    def run_pipeline():
        x_train, y_train, x_test, y_test = load_and_preprocess_data()
        model = build_model()
        train_model(model)
        evaluate_model(model)
        save_model(model)

    # Define the pipeline
    mnist_training_pipeline()
