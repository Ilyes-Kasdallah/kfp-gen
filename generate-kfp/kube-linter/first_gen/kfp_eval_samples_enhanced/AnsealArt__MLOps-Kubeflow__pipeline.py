import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error


# Define the pipeline function
@dsl.pipeline(name="California Housing Prediction Pipeline")
def california_housing_prediction_pipeline(
    output_path: str,
    run_date: str,
    test_size: float = 0.2,
):
    # Step 1: Download and preprocess data
    @component
    def download_and_preprocess_data(
        output_path: str, run_date: str, test_size: float = 0.2
    ):
        # Load the California housing dataset
        data = fetch_california_housing()

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=test_size, random_state=42
        )

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Save the preprocessed data to a file
        with open(output_path, "wb") as f:
            f.write(X_train_scaled.to_numpy().tobytes())
            f.write(y_train.to_numpy().tobytes())

    # Step 2: Train the model
    @component
    def train_model(X_train_scaled, y_train):
        # Initialize the model
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()

        # Train the model
        model.fit(X_train_scaled, y_train)

        # Return the trained model
        return model

    # Step 3: Make predictions
    @component
    def make_predictions(model, X_test_scaled):
        # Make predictions on the test set
        predictions = model.predict(X_test_scaled)

        # Return the predictions
        return predictions

    # Step 4: Evaluate the model
    @component
    def evaluate_model(predictions, y_test):
        # Calculate the mean squared error
        mse = mean_squared_error(y_test, predictions)

        # Return the mean squared error
        return mse


# Run the pipeline
if __name__ == "__main__":
    pipeline.run()
