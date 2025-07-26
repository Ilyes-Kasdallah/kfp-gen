
from kfp import pipeline
from kfp.components import script

@pipeline(name="sms_spam_classifier")
def sms_spam_classifier():
    # Define the extract_data component
    @script(name="extract_data")
    def extract_data():
        # Download the zip file from the public URL
        import requests
        response = requests.get("https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip")
        with open("sms_spam_collection.zip", "wb") as f:
            f.write(response.content)
        return "sms_spam_collection.zip"

    # Define the model training component
    @script(name="model_training")
    def model_training():
        # Load the dataset
        import pandas as pd
        data = pd.read_csv("sms_spam_collection.csv")
        # Split the dataset into features and labels
        X = data.drop(columns=["label"])
        y = data["label"]
        # Train a simple machine learning model
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Train the model
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()
        model.fit(X_train, y_train)
        return model

    # Define the model evaluation component
    @script(name="model_evaluation")
    def model_evaluation(model):
        # Evaluate the model on the test set
        from sklearn.metrics import accuracy_score
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy

    # Define the pipeline execution
    @script(name="pipeline_execution")
    def pipeline_execution():
        # Extract the data
        extracted_data = extract_data()
        # Train the model
        trained_model = model_training()
        # Evaluate the model
        accuracy = model_evaluation(trained_model)
        print(f"Model accuracy: {accuracy}")

# Execute the pipeline
pipeline_execution()
