import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from google.cloud import storage
from tensorflow import estimator
from tensorflow.keras.preprocessing import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam


# Define the pipeline function
@dsl.pipeline(name="Santander Customer Transaction Prediction")
def santander_customer_transaction_prediction(
    train_path: str,
    evaluation_path: str,
    model_name: str = "santander-trnx-classification",
    epochs: int = 10,
    batch_size: int = 32,
    validation_split: float = 0.2,
    learning_rate: float = 0.001,
    dropout_rate: float = 0.2,
    max_steps: int = 10000,
):
    # Load the training and evaluation data
    train_data = estimator.load_dataset(train_path)
    evaluation_data = estimator.load_dataset(evaluation_path)

    # Split the data into training and validation sets
    train_data, validation_data = train_test_split(
        train_data, test_size=validation_split, random_state=42
    )

    # Build the model
    model = Sequential(
        [
            Dense(64, activation="relu", input_shape=(train_data.shape[1],)),
            Dropout(dropout_rate),
            Dense(32, activation="relu"),
            Dropout(dropout_rate),
            Dense(1, activation="sigmoid"),
        ]
    )

    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate), loss="binary_crossentropy", metrics=["accuracy"]
    )

    # Train the model
    model.fit(
        train_data,
        validation_data,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        max_steps=max_steps,
    )

    # Evaluate the model
    predictions = model.predict(validation_data)
    accuracy = (predictions == validation_data["label"]).mean()
    print(f"Validation Accuracy: {accuracy:.2f}")


# Example usage
if __name__ == "__main__":
    santander_customer_transaction_prediction(
        train_path="gs://your-bucket/train.csv",
        evaluation_path="gs://your-bucket/evaluation.csv",
    )
