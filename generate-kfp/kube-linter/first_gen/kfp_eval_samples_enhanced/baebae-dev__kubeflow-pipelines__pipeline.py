import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error


# Define the pipeline function
@dsl.pipeline(name="Boston Housing Pipeline")
def BostonHousingPipeline():
    # Load the Boston housing dataset
    x_train, x_test = load_boston()

    # Split the data into training and testing sets
    x_train, x_test = train_test_split(x_train, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Define the model
    @component
    def predict_model(x_train_scaled):
        # Build and train the model
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(x_train_scaled, y_train)
        return model

    # Predict on the test set
    @component
    def predict_on_test(model):
        # Make predictions on the test set
        y_pred = model.predict(x_test_scaled)
        return y_pred

    # Return the predictions
    @component
    def get_predictions(y_pred):
        # Return the predictions
        return y_pred.tolist()


# Run the pipeline
if __name__ == "__main__":
    pipeline.run()
