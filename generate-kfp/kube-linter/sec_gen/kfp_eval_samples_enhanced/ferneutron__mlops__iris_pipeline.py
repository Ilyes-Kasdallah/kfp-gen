import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="The-Iris-Pipeline-v1")
def iris_pipeline(project_id, bq_dataset, bq_table):
    # Load data from BigQuery
    train_dataset = component(
        name="load_train_dataset",
        description="Loads the Iris dataset from BigQuery.",
        inputs={
            "project_id": Input(str(project_id)),
            "bq_dataset": Input(str(bq_dataset)),
            "bq_table": Input(str(bq_table)),
        },
        outputs={"train_dataset": Output(Dataset(type=DatasetType.PATH))},
        steps=[
            component(
                name="load_data",
                description="Loads the Iris dataset from BigQuery.",
                inputs={
                    "project_id": Input(str(project_id)),
                    "bq_dataset": Input(str(bq_dataset)),
                    "bq_table": Input(str(bq_table)),
                },
                outputs={"data": Output(Dataset(type=DatasetType.PATH))},
                steps=[
                    component(
                        name="read_csv",
                        description="Reads the CSV file into a Pandas DataFrame.",
                        inputs={"data": Input(Dataset(type=DatasetType.PATH))},
                        outputs={"df": Output(Dataset(type=DatasetType.PATH))},
                        steps=[
                            component(
                                name="filter_data",
                                description="Filters the DataFrame to include only the Iris dataset.",
                                inputs={"df": Input(Dataset(type=DatasetType.PATH))},
                                outputs={
                                    "filtered_df": Output(
                                        Dataset(type=DatasetType.PATH)
                                    )
                                },
                                steps=[
                                    component(
                                        name="drop_columns",
                                        description="Drops unnecessary columns from the filtered DataFrame.",
                                        inputs={
                                            "filtered_df": Input(
                                                Dataset(type=DatasetType.PATH)
                                            )
                                        },
                                        outputs={
                                            "dropped_df": Output(
                                                Dataset(type=DatasetType.PATH)
                                            )
                                        },
                                        steps=[
                                            component(
                                                name="select_columns",
                                                description="Selects the necessary columns from the dropped DataFrame.",
                                                inputs={
                                                    "dropped_df": Input(
                                                        Dataset(type=DatasetType.PATH)
                                                    )
                                                },
                                                outputs={
                                                    "selected_df": Output(
                                                        Dataset(type=DatasetType.PATH)
                                                    )
                                                },
                                                steps=[
                                                    component(
                                                        name="convert_to_pandas",
                                                        description="Converts the selected DataFrame to a Pandas DataFrame.",
                                                        inputs={
                                                            "selected_df": Input(
                                                                Dataset(
                                                                    type=DatasetType.PATH
                                                                )
                                                            )
                                                        },
                                                        outputs={
                                                            "pandas_df": Output(
                                                                Dataset(
                                                                    type=DatasetType.PATH
                                                                )
                                                            )
                                                        },
                                                        steps=[
                                                            component(
                                                                name="save_to_csv",
                                                                description="Saves the Pandas DataFrame to a CSV file.",
                                                                inputs={
                                                                    "pandas_df": Input(
                                                                        Dataset(
                                                                            type=DatasetType.PATH
                                                                        )
                                                                    ),
                                                                    "output_file": Output(
                                                                        Dataset(
                                                                            type=DatasetType.PATH
                                                                        )
                                                                    ),
                                                                },
                                                                outputs={
                                                                    "csv_file": Output(
                                                                        Dataset(
                                                                            type=DatasetType.PATH
                                                                        )
                                                                    )
                                                                },
                                                            )
                                                        ],
                                                    )
                                                ],
                                            )
                                        ],
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Compile the pipeline
    kfp.compiler.Compiler().compile(iris_pipeline, pipeline_root)
