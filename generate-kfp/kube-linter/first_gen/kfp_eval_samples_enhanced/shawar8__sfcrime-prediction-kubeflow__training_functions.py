import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# Define the training pipeline
@dsl.pipeline(name="training_pipeline")
def training_pipeline(df_path, label_column, test_size, n_tries):
    # Define the get_train_test_split component
    @component
    def get_train_test_split(df_path, label_column, test_size, n_tries):
        # Load the dataset
        df = pd.read_csv(df_path)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            df.drop(label_column, axis=1),
            df[label_column],
            test_size=test_size,
            random_state=42,
            shuffle=True,
            n_trials=n_tries,
        )

        return X_train, X_test, y_train, y_test

    # Define the model training component
    @component
    def model_training(X_train, X_test, y_train, y_test):
        # Initialize the model
        model = Sequential(
            [
                Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
                Dense(32, activation="relu"),
                Dense(1, activation="sigmoid"),
            ]
        )

        # Compile the model
        model.compile(
            optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
        )

        # Train the model
        model.fit(
            X_train,
            y_train,
            epochs=100,
            batch_size=32,
            validation_data=(X_test, y_test),
        )

        return model

    # Define the pipeline
    @pipeline
    def pipeline():
        # Get the training data
        X_train, X_test, y_train, y_test = get_train_test_split(
            df_path, label_column, test_size, n_tries
        )

        # Train the model
        model = model_training(X_train, X_test, y_train, y_test)

        return model


# Example usage
if __name__ == "__main__":
    # Replace 'path_to_your_dataset.csv' with the actual path to your dataset
    df_path = "path_to_your_dataset.csv"

    # Replace 'your_label_column' with the actual label column name
    label_column = "your_label_column"

    # Replace 'test_size' with the desired test size
    test_size = 0.2

    # Replace 'n_tries' with the desired number of training trials
    n_tries = 5

    # Run the pipeline
    trained_model = pipeline()
    print("Model trained successfully.")
