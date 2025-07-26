import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# Define the pipeline function
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data from two specified URLs
    @component
    def load_data(url1, url2):
        # Load data from URLs
        data = load_diabetes()
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    # Clean and preprocess the data
    @component
    def clean_and_preprocess_data(X_train, X_test, y_train, y_test):
        # Handle missing values
        X_train = X_train.dropna()
        X_test = X_test.dropna()

        # Convert categorical features to numerical representations
        categorical_features = ["age", "sex", "bmi"]
        transformer = ColumnTransformer(
            transformers=[
                ("age", "category", {"cat": ["age"]}),
                ("sex", "category", {"cat": ["sex"]}),
                ("bmi", "scale", {"scale": [0, 1]}),
            ],
            remainder="passthrough",
        )
        X_train = transformer.fit_transform(X_train)
        X_test = transformer.transform(X_test)

        # Scale the features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        return X_train, X_test, y_train, y_test

    # Save the cleaned dataset as a CSV file
    @component
    def save_cleaned_dataset(X_train, X_test, y_train, y_test):
        # Save the cleaned dataset as a CSV file
        X_train.to_csv("diabetes_train.csv", index=False)
        X_test.to_csv("diabetes_test.csv", index=False)
        return X_train, X_test, y_train, y_test

    # Main function to run the pipeline
    @component
    def main(X_train, X_test, y_train, y_test):
        # Predict diabetes
        model = load_model("diabetes_model")
        predictions = model.predict(X_test)
        return predictions


# Run the pipeline
diabetes_prediction_pipeline().run()
