
from kfp import dsl

@dsl.pipeline(name="lightweight_python_functions_v2")
def lightweight_python_functions_v2_pipeline():
    # Define the preprocess component
    preprocess = dsl.component(
        name="preprocess",
        description="Preprocesses the input message",
        inputs={
            "message": dsl.Input("message", type=dsl.StringType())
        },
        outputs={
            "output_dataset_one": dsl.Output("output_dataset_one", type=dsl.DatasetType())
        },
        steps=[
            dsl.task(
                name="split_message",
                description="Splits the message into two parts",
                inputs={
                    "message": dsl.Input("message", type=dsl.StringType())
                },
                outputs={
                    "part1": dsl.Output("part1", type=dsl.StringType()),
                    "part2": dsl.Output("part2", type=dsl.StringType())
                },
                steps=[
                    dsl.task(
                        name="remove_punctuation",
                        description="Removes punctuation from the message",
                        inputs={
                            "message": dsl.Input("message", type=dsl.StringType())
                        },
                        outputs={
                            "cleaned_message": dsl.Output("cleaned_message", type=dsl.StringType())
                        },
                        steps=[
                            dsl.task(
                                name="lowercase",
                                description="Converts the message to lowercase",
                                inputs={
                                    "cleaned_message": dsl.Input("cleaned_message", type=dsl.StringType())
                                },
                                outputs={
                                    "lowercased_message": dsl.Output("lowercased_message", type=dsl.StringType())
                                }
                            ),
                            dsl.task(
                                name="strip_whitespace",
                                description="Strips any leading or trailing whitespace",
                                inputs={
                                    "lowercased_message": dsl.Input("lowercased_message", type=dsl.StringType())
                                },
                                outputs={
                                    "stripped_message": dsl.Output("stripped_message", type=dsl.StringType())
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Define the model training component
    train_model = dsl.component(
        name="train_model",
        description="Trains a simple linear regression model",
        inputs={
            "input_dataset_one": dsl.Input("input_dataset_one", type=dsl.DatasetType())
        },
        outputs={
            "model": dsl.Output("model", type=dsl.ModelType())
        },
        steps=[
            dsl.task(
                name="load_data",
                description="Loads the dataset",
                inputs={
                    "input_dataset_one": dsl.Input("input_dataset_one", type=dsl.DatasetType())
                },
                outputs={
                    "data": dsl.Output("data", type=dsl.TensorType())
                },
                steps=[
                    dsl.task(
                        name="split_data",
                        description="Splits the data into features and labels",
                        inputs={
                            "data": dsl.Input("data", type=dsl.TensorType())
                        },
                        outputs={
                            "features": dsl.Output("features", type=dsl.TensorType()),
                            "labels": dsl.Output("labels", type=dsl.TensorType())
                        },
                        steps=[
                            dsl.task(
                                name="normalize_features",
                                description="Normalizes the features",
                                inputs={
                                    "features": dsl.Input("features", type=dsl.TensorType())
                                },
                                outputs={
                                    "normalized_features": dsl.Output("normalized_features", type=dsl.TensorType())
                                }
                            ),
                            dsl.task(
                                name="split_labels",
                                description="Splits the labels into training and testing sets",
                                inputs={
                                    "labels": dsl.Input("labels", type=dsl.TensorType())
                                },
                                outputs={
                                    "training_labels": dsl.Output("training_labels", type=dsl.TensorType()),
                                    "testing_labels": dsl.Output("testing_labels", type=dsl.TensorType())
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Define the pipeline
    return preprocess >> train_model
