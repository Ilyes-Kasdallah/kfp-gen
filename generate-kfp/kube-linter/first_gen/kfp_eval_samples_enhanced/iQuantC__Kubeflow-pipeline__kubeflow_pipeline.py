import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dsl.pipeline(name="iris_pipeline")
def iris_pipeline():
    # Load the Iris dataset
    data = load_iris()

    # Convert the dataset to a Pandas DataFrame
    df = pd.DataFrame(data.data, columns=data.feature_names)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        df, data.target, test_size=0.2, random_state=42
    )

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define the model
    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression()

    # Train the model
    model.fit(X_train_scaled, y_train)

    # Evaluate the model
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model accuracy: {accuracy:.2f}")


# Run the pipeline
iris_pipeline()
