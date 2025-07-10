from click import Tuple
from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn", "tensorflow"]
)
def load_data() -> Dataset:
    df = pd.read_csv('data.csv')
    return df


@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn", "tensorflow"]
)
def preprocess_data(df: Dataset) -> Tuple[Dataset, Dataset]:
    X = df.drop(columns=['target'])
    y = df['target']
    return train_test_split(X, y, test_size=0.2)


@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn", "tensorflow"]
)
def train_model(X_train: Dataset, y_train: Dataset) -> Model:
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model


@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn", "tensorflow"]
)
def save_model(model: Dataset) -> Dataset:
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)


@dsl.pipeline(name="ml-pipeline")
def ml_pipeline():
    df = load_data()
    X_train, y_train = preprocess_data(df.output)
    model = train_model(X_train.output, y_train.output)
    output = save_model(model.output)

if __name__ == "__main__":
    from kfp import compiler
    compiler.Compiler().compile(ml_pipeline, "ml_pipeline.yaml")
