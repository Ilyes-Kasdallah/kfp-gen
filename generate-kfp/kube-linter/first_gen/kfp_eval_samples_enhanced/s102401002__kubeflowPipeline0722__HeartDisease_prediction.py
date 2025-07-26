import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the HeartDiseasePrediction pipeline
@pipeline(name="HeartDiseasePrediction")
def HeartDiseasePrediction():
    # Load data from a CSV file
    @component
    def load_data(url):
        df = pd.read_csv(url)
        return df

    # Split the data into training and testing sets
    @component
    def split_data(df):
        X = df.drop("target", axis=1)
        y = df["target"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    # Standardize the features
    @component
    def standardize_features(X_train, X_test):
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    # Train a logistic regression model
    @component
    def train_model(X_train_scaled, y_train):
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train_scaled, y_train)
        return model

    # Evaluate the model
    @component
    def evaluate_model(model, X_test_scaled, y_test):
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy

    # Main function to run the pipeline
    @component
    def main():
        df = load_data(
            "https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/heart_2020_cleaned.csv"
        )
        X_train, X_test, y_train, y_test = split_data(df)
        X_train_scaled, X_test_scaled = standardize_features(X_train, X_test)
        model = train_model(X_train_scaled, y_train)
        accuracy = evaluate_model(model, X_test_scaled, y_test)
        print(f"Accuracy: {accuracy}")


# Run the pipeline
if __name__ == "__main__":
    main()
