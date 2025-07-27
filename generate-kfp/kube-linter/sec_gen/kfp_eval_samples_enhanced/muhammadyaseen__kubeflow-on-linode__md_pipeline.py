import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="md-pipeline")
def md_pipeline():
    # Define the first component
    write_simple_markdown_table = component(
        name="write_simple_markdown_table",
        description="This component creates a Markdown file containing a simple table with animal names.",
        inputs={
            "animal_names": Input(type=Output[Dataset]),
        },
        outputs={
            "markdown_artifact": Output(type=Output[Model]),
        },
        steps=[
            component(
                name="generate_markdown_table",
                description="This step generates a Markdown table from the input animal names.",
                inputs={
                    "animal_names": Input(type=Input[Dataset]),
                },
                outputs={
                    "markdown_table": Output(type=Output[Model]),
                },
                steps=[
                    component(
                        name="format_markdown_table",
                        description="This step formats the Markdown table into a readable string.",
                        inputs={
                            "markdown_table": Input(type=Input[Model]),
                        },
                        outputs={
                            "markdown_string": Output(type=Output[str]),
                        },
                        steps=[
                            component(
                                name="write_to_file",
                                description="This step writes the formatted Markdown table to a file.",
                                inputs={
                                    "markdown_string": Input(type=Input[str]),
                                    "output_path": Input(type=Output[Dataset]),
                                },
                                outputs={
                                    "output_path": Output(type=Output[Dataset]),
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    # Define the second component
    write_to_file = component(
        name="write_to_file",
        description="This component writes the formatted Markdown table to a file.",
        inputs={
            "markdown_string": Input(type=Input[str]),
            "output_path": Input(type=Output[Dataset]),
        },
        outputs={
            "output_path": Output(type=Output[Dataset]),
        },
        steps=[
            component(
                name="format_markdown_table",
                description="This step formats the Markdown table into a readable string.",
                inputs={
                    "markdown_table": Input(type=Input[Model]),
                },
                outputs={
                    "markdown_string": Output(type=Output[str]),
                },
                steps=[
                    component(
                        name="write_to_file",
                        description="This step writes the formatted Markdown table to a file.",
                        inputs={
                            "markdown_string": Input(type=Input[str]),
                            "output_path": Input(type=Output[Dataset]),
                        },
                        outputs={
                            "output_path": Output(type=Output[Dataset]),
                        },
                    ),
                ],
            ),
        ],
    )

    # Define the third component
    format_markdown_table = component(
        name="format_markdown_table",
        description="This step formats the Markdown table into a readable string.",
        inputs={
            "markdown_table": Input(type=Input[Model]),
        },
        outputs={
            "markdown_string": Output(type=Output[str]),
        },
        steps=[
            component(
                name="write_to_file",
                description="This step writes the formatted Markdown table to a file.",
                inputs={
                    "markdown_string": Input(type=Input[str]),
                    "output_path": Input(type=Output[Dataset]),
                },
                outputs={
                    "output_path": Output(type=Output[Dataset]),
                },
            ),
        ],
    )

    # Define the fourth component
    write_to_file = component(
        name="write_to_file",
        description="This component writes the formatted Markdown table to a file.",
        inputs={
            "markdown_string": Input(type=Input[str]),
            "output_path": Input(type=Output[Dataset]),
        },
        outputs={
            "output_path": Output(type=Output[Dataset]),
        },
        steps=[
            component(
                name="format_markdown_table",
                description="This step formats the Markdown table into a readable string.",
                inputs={
                    "markdown_table": Input(type=Input[Model]),
                },
                outputs={
                    "markdown_string": Output(type=Output[str]),
                },
                steps=[
                    component(
                        name="write_to_file",
                        description="This step writes the formatted Markdown table to a file.",
                        inputs={
                            "markdown_string": Input(type=Input[str]),
                            "output_path": Input(type=Output[Dataset]),
                        },
                        outputs={
                            "output_path": Output(type=Output[Dataset]),
                        },
                    ),
                ],
            ),
        ],
    )

    # Call the components
    write_simple_markdown_table(animal_names="dog cat elephant")
    write_to_file(markdown_string="Here's a simple table:")
    format_markdown_table(markdown_table="Here's a more complex table:")
    write_to_file(markdown_string="Here's a final table:")
