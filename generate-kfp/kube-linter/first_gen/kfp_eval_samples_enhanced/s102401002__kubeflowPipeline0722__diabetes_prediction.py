import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Define the pipeline function
@pipeline(name="diabetes_prediction")
def diabetes_prediction():
    # Load data from CSV files
    data1 = component.load_data("data1.csv")
    data2 = component.load_data("10k.csv")

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data1, data2, test_size=0.2, random_state=42
    )

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")


# Run the pipeline
diabetes_prediction()
