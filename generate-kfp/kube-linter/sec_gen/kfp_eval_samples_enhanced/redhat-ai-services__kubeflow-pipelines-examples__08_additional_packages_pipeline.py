import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


@dsl.component
def get_iris_data():
    """
    Loads the Iris dataset from scikit-learn, converts it into a Pandas DataFrame with columns "sepalLength", "sepalWidth", "petalLength", "petalWidth", and "species".
    Also, prints the head of the DataFrame.
    """
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["species"] = iris.target
    print(df.head())
    return df


@dsl.pipeline(name="Additional Packages Pipeline")
def additional_packages_pipeline():
    """
    This pipeline includes one component: 1. `get_iris_data` component.
    """
    iris_data = get_iris_data()

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris_data.drop("species"), iris_data["species"], test_size=0.2, random_state=42
    )

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train a model
    model = Model.from_pretrained("sklearn-iris")
    model.fit(X_train_scaled, y_train)

    # Evaluate the model
    metrics = model.evaluate(X_test_scaled, y_test)
    print(metrics)


if __name__ == "__main__":
    pipeline_root = "gs://my-bucket/pipeline-root"
    pipeline = additional_packages_pipeline()
    pipeline.run(pipeline_root=pipeline_root)
