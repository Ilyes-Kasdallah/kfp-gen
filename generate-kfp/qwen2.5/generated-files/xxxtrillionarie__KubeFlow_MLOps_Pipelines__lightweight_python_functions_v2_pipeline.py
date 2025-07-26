
from kfp import dsl

@dsl.pipeline(name="lightweight_python_functions_v2")
def lightweight_python_functions_v2_pipeline():
    # Define the preprocess component
    preprocess = dsl.component(
        name="preprocess",
        description="Preprocesses the input message.",
        inputs={
            "input_message": dsl.Input("input_message", type="string"),
        },
        outputs={
            "output_dataset_one": dsl.Output("output_dataset_one", type="Dataset"),
        },
        steps=[
            dsl.task(
                name="split_message",
                description="Splits the input message into two parts.",
                inputs={
                    "input_message": dsl.Input("input_message", type="string"),
                },
                outputs={
                    "part1": dsl.Output("part1", type="string"),
                    "part2": dsl.Output("part2", type="string"),
                },
                steps=[
                    dsl.task(
                        name="remove_punctuation",
                        description="Removes punctuation from the input message.",
                        inputs={
                            "input_message": dsl.Input("input_message", type="string"),
                        },
                        outputs={
                            "cleaned_message": dsl.Output("cleaned_message", type="string"),
                        },
                        steps=[
                            dsl.task(
                                name="lowercase",
                                description="Converts the cleaned message to lowercase.",
                                inputs={
                                    "cleaned_message": dsl.Input("cleaned_message", type="string"),
                                },
                                outputs={
                                    "lowercased_message": dsl.Output("lowercased_message", type="string"),
                                },
                            ),
                            dsl.task(
                                name="strip_whitespace",
                                description="Strips any leading or trailing whitespace from the cleaned message.",
                                inputs={
                                    "lowercased_message": dsl.Input("lowercased_message", type="string"),
                                },
                                outputs={
                                    "stripped_message": dsl.Output("stripped_message", type="string"),
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    # Define the model training component
    train_model = dsl.component(
        name="train_model",
        description="Trains a simple linear regression model on the cleaned message.",
        inputs={
            "cleaned_message": dsl.Input("cleaned_message", type="string"),
        },
        outputs={
            "model": dsl.Output("model", type="PipelineModel"),
        },
        steps=[
            dsl.task(
                name="load_data",
                description="Loads the dataset from a file.",
                inputs={
                    "cleaned_message": dsl.Input("cleaned_message", type="string"),
                },
                outputs={
                    "dataset": dsl.Output("dataset", type="Dataset"),
                },
                steps=[
                    dsl.task(
                        name="read_csv",
                        description="Reads the CSV file into a Dataset.",
                        inputs={
                            "dataset": dsl.Input("dataset", type="Dataset"),
                        },
                        outputs={
                            "csv_dataset": dsl.Output("csv_dataset", type="Dataset"),
                        },
                    ),
                ],
            ),
            dsl.task(
                name="split_dataset",
                description="Splits the dataset into training and testing sets.",
                inputs={
                    "csv_dataset": dsl.Input("csv_dataset", type="Dataset"),
                },
                outputs={
                    "train_dataset": dsl.Output("train_dataset", type="Dataset"),
                    "test_dataset": dsl.Output("test_dataset", type="Dataset"),
                },
                steps=[
                    dsl.task(
                        name="random_split",
                        description="Randomly splits the dataset into training and testing sets.",
                        inputs={
                            "csv_dataset": dsl.Input("csv_dataset", type="Dataset"),
                        },
                        outputs={
                            "train_dataset": dsl.Output("train_dataset", type="Dataset"),
                            "test_dataset": dsl.Output("test_dataset", type="Dataset"),
                        },
                    ),
                ],
            ),
            dsl.task(
                name="train_model",
                description="Trains a simple linear regression model on the training set.",
                inputs={
                    "train_dataset": dsl.Input("train_dataset", type="Dataset"),
                },
                outputs={
                    "model": dsl.Output("model", type="PipelineModel"),
                },
                steps=[
                    dsl.task(
                        name="fit_model",
                        description="Fits the linear regression model to the training data.",
                        inputs={
                            "model": dsl.Input("model", type="PipelineModel"),
                            "train_dataset": dsl.Input("train_dataset", type="Dataset"),
                        },
                        outputs={
                            "trained_model": dsl.Output("trained_model", type="PipelineModel"),
                        },
                    ),
                ],
            ),
        ],
    )

    # Define the pipeline
    return dsl.Pipeline(
        name="lightweight_python_functions_v2",
        components=[preprocess, train_model],
    )
