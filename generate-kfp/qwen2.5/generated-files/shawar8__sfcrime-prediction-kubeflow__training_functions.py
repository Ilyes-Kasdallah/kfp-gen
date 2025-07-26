
from kfp import dsl

@dsl.pipeline(name="training_pipeline")
def training_pipeline(
    df_path: str,
    label_column: str,
    test_size: float,
    n_tries: int,
    training_functions: str = "training_functions",
):
    # Define the get_train_test_split component
    get_train_test_split = dsl.component(
        name="get_train_test_split",
        description="This component splits the dataset into training and testing sets.",
        inputs={
            "df_path": df_path,
            "label_column": label_column,
            "test_size": test_size,
            "n_tries": n_tries,
        },
        outputs={"train_data": "pandas.DataFrame", "test_data": "pandas.DataFrame"},
    )

    # Define the training function component
    training_function = dsl.component(
        name=training_functions,
        description="This component trains a machine learning model.",
        inputs={
            "train_data": "pandas.DataFrame",
            "test_data": "pandas.DataFrame",
        },
        outputs={"model": "tensorflow.keras.Model"},
    )

    # Define the pipeline
    pipeline = dsl.Pipeline(
        name="training_pipeline",
        steps=[
            get_train_test_split,
            training_function,
        ],
    )

    return pipeline
