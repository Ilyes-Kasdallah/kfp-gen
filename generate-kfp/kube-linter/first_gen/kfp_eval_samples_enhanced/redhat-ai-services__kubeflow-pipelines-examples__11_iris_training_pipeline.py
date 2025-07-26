import kfp
from kfp.dsl import pipeline, component

# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@component
def data_prep(data):
    """
    Preprocesses the Iris dataset.

    Args:
    data (pandas.DataFrame): The Iris dataset loaded from sklearn.datasets.load_iris.

    Returns:
    pandas.DataFrame: The preprocessed dataset.
    """
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data, target="species", test_size=0.3, random_state=42
    )

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return pd.DataFrame(
        {
            "X_train": X_train_scaled,
            "X_test": X_test_scaled,
            "y_train": y_train,
            "y_test": y_test,
        }
    )


@pipeline(name="11_iris_training_pipeline")
def iris_training_pipeline():
    """
    Pipeline to train an ML model on the Iris dataset.

    Returns:
    None
    """
    # Load the Iris dataset
    iris_data = load_iris()

    # Preprocess the data
    preprocessed_data = data_prep(iris_data)

    # Train a simple linear regression model
    from sklearn.linear_model import LinearRegression

    model = LinearRegression()
    model.fit(preprocessed_data[["X_train", "X_test"]], preprocessed_data["y_train"])

    # Evaluate the model
    print("Model Evaluation:")
    print(
        f"Mean Squared Error: {model.score(preprocessed_data[['X_test', 'y_test']], preprocessed_data['y_test'])}"
    )


# Run the pipeline
iris_training_pipeline()
