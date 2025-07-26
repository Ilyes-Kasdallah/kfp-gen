import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier


# Define the pipeline function
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data
    @component
    def load_data():
        # Load diabetes dataset from URLs
        diabetes_data = load_diabetes()
        return diabetes_data

    # Split data into training and testing sets
    @component
    def split_data(diabetes_data):
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            diabetes_data.data, diabetes_data.target, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    # Standardize features
    @component
    def standardize_features(X_train, X_test):
        # Standardize features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    # Train XGBoost model
    @component
    def train_model(X_train_scaled, y_train):
        # Train XGBoost model
        model = XGBClassifier(n_estimators=100, learning_rate=0.01, random_state=42)
        model.fit(X_train_scaled, y_train)
        return model

    # Evaluate the model
    @component
    def evaluate_model(model, X_test_scaled, y_test):
        # Evaluate the model
        predictions = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, predictions)
        return accuracy

    # Main function to run the pipeline
    @component
    def main():
        # Load data
        diabetes_data = load_data()
        X_train, X_test, y_train, y_test = split_data(diabetes_data)
        X_train_scaled, X_test_scaled = standardize_features(X_train, X_test)

        # Train model
        model = train_model(X_train_scaled, y_train)

        # Evaluate the model
        accuracy = evaluate_model(model, X_test_scaled, y_test)

        # Print the accuracy
        print(f"Accuracy: {accuracy}")


# Run the pipeline
diabetes_prediction_pipeline().run()
