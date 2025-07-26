import kfp
from kfp.dsl import pipeline, component

# Import necessary libraries
from google.cloud import bigquery
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# Define the pipeline
@dsl.pipeline(name="Time-Series-Forecast-Chicago-Taxi")
def time_series_forecast_chicago_taxi():
    # Read metadata from BigQuery
    @component
    def read_metadata():
        client = bigquery.Client()
        query = """
        SELECT 
            community_area,
            z_normalized_statistics
        FROM 
            chicago_taxi_data
        """
        df = client.query(query).to_dataframe()
        return df

    # Normalize z-normalized statistics
    @component
    def normalize_z_statistics(df):
        scaler = StandardScaler()
        df["z_normalized_statistics"] = scaler.fit_transform(
            df[["z_normalized_statistics"]]
        )
        return df

    # Split data into training and testing sets
    @component
    def split_data(df):
        X = df.drop("z_normalized_statistics", axis=1)
        y = df["z_normalized_statistics"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    # Train a linear regression model
    @component
    def train_linear_regression(X_train, y_train):
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(X_train, y_train)
        return model

    # Make predictions
    @component
    def make_predictions(model, X_test):
        predictions = model.predict(X_test)
        return predictions

    # Evaluate the model
    @component
    def evaluate_model(predictions, y_test):
        mse = mean_squared_error(y_test, predictions)
        return mse


# Build the pipeline
build_pipeline(time_series_forecast_chicago_taxi)
