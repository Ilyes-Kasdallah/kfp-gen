
from kfp import dsl

@dsl.pipeline(name="data_ingestion_pipeline")
def data_ingestion_pipeline(
    df_path: str,
    to_keep: list,
    data: str = "train",
):
    # Define the preprocess_data component
    preprocess_data = dsl.component(
        name="preprocess_data",
        description="Preprocesses the data for training or serving.",
        inputs={
            "df_path": df_path,
            "to_keep": to_keep,
            "data": data,
        },
        outputs={"processed_df": dsl.output_type("pandas.DataFrame")},
    )

    # Define the main component
    main_component = dsl.component(
        name="main_component",
        description="Main component that orchestrates the pipeline.",
        inputs={
            "processed_df": preprocess_data.outputs["processed_df"],
        },
        outputs={"labelled_df": dsl.output_type("pandas.DataFrame")},
    )

    # Define the final component
    final_component = dsl.component(
        name="final_component",
        description="Final component that labels the data.",
        inputs={
            "labelled_df": main_component.outputs["labelled_df"],
        },
        outputs={"output_file": dsl.output_type("string")},
    )

    # Execute the pipeline
    with dsl.PipelineExecutor() as executor:
        executor.submit(main_component, df_path, to_keep, data)
        executor.submit(final_component, main_component.outputs["labelled_df"], output_file)
