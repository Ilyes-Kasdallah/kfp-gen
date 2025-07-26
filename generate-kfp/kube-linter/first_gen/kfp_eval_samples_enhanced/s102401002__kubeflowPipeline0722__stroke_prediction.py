import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the pipeline function
@pipeline(name="Stroke Prediction Pipeline")
def stroke_prediction():
    # Load data from CSV files
    @component
    def load_data():
        data = kfp.io.text_file(
            "https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/stroke.csv"
        )
        return data

    # Split data into training and testing sets
    @component
    def split_data(data):
        X, y = data.read_csv().drop(columns=["stroke"])
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test

    # Preprocess data
    @component
    def preprocess_data(X_train, X_test):
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    # Train logistic regression model
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
        X_train, X_test, y_train, y_test = split_data(load_data())
        X_train_scaled, X_test_scaled = preprocess_data(X_train, X_test)
        model = train_model(X_train_scaled, y_train)
        accuracy = evaluate_model(model, X_test_scaled, y_test)
        print(f"Accuracy: {accuracy}")


# Run the pipeline
if __name__ == "__main__":
    main()
