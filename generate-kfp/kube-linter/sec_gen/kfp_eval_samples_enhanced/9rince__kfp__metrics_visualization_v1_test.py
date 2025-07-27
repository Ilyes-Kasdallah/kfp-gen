import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="metrics_visualization_v1_pipeline")
def metrics_visualization_v1_test():
    # Define the table visualization component
    table_visualization = component(
        name="table-visualization",
        description="Visualize data using a table",
        inputs=[
            Input("data", type=Input.Dataset),
            Input("columns", type=Input.Dataset),
        ],
        outputs=[Output("mlpipeline_ui_metadata", type=Output.Dataset)],
        steps=[
            component(
                name="generate_table",
                description="Generate a table from the input dataset",
                inputs=[Input("dataset", type=Input.Dataset)],
                outputs=[Output("table", type=Output.Dataset)],
                steps=[
                    component(
                        name="format_table",
                        description="Format the table into a readable string",
                        inputs=[Input("table", type=Input.Dataset)],
                        outputs=[Output("formatted_table", type=Output.Dataset)],
                        steps=[
                            component(
                                name="display_table",
                                description="Display the formatted table",
                                inputs=[Input("formatted_table", type=Input.Dataset)],
                                outputs=[
                                    Output(
                                        "mlpipeline_ui_metadata", type=Output.Dataset
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    # Define the markdown visualization component
    markdown_visualization = component(
        name="markdown-visualization",
        description="Visualize data using Markdown",
        inputs=[Input("data", type=Input.Dataset), Input("title", type=Input.String)],
        outputs=[Output("mlpipeline_ui_metadata", type=Output.Dataset)],
        steps=[
            component(
                name="generate_markdown",
                description="Generate a Markdown string from the input dataset",
                inputs=[Input("dataset", type=Input.Dataset)],
                outputs=[Output("markdown", type=Output.Dataset)],
                steps=[
                    component(
                        name="format_markdown",
                        description="Format the Markdown string into a readable string",
                        inputs=[Input("markdown", type=Input.Dataset)],
                        outputs=[Output("formatted_markdown", type=Output.Dataset)],
                        steps=[
                            component(
                                name="display_markdown",
                                description="Display the formatted Markdown string",
                                inputs=[
                                    Input("formatted_markdown", type=Input.Dataset)
                                ],
                                outputs=[
                                    Output(
                                        "mlpipeline_ui_metadata", type=Output.Dataset
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    # Define the roc-visualization component
    roc_visualization = component(
        name="roc-visualization",
        description="Visualize data using ROC curve",
        inputs=[
            Input("data", type=Input.Dataset),
            Input("thresholds", type=Input.Dataset),
        ],
        outputs=[Output("mlpipeline_ui_metadata", type=Output.Dataset)],
        steps=[
            component(
                name="generate_roc_curve",
                description="Generate a ROC curve from the input dataset",
                inputs=[Input("dataset", type=Input.Dataset)],
                outputs=[Output("roc_curve", type=Output.Dataset)],
                steps=[
                    component(
                        name="plot_roc_curve",
                        description="Plot the ROC curve",
                        inputs=[Input("roc_curve", type=Input.Dataset)],
                        outputs=[Output("mlpipeline_ui_metadata", type=Output.Dataset)],
                    )
                ],
            )
        ],
    )

    # Define the html-visualization component
    html_visualization = component(
        name="html-visualization",
        description="Visualize data using HTML",
        inputs=[Input("data", type=Input.Dataset), Input("title", type=Input.String)],
        outputs=[Output("mlpipeline_ui_metadata", type=Output.Dataset)],
        steps=[
            component(
                name="generate_html",
                description="Generate an HTML string from the input dataset",
                inputs=[Input("dataset", type=Input.Dataset)],
                outputs=[Output("html", type=Output.Dataset)],
                steps=[
                    component(
                        name="format_html",
                        description="Format the HTML string into a readable string",
                        inputs=[Input("html", type=Input.Dataset)],
                        outputs=[Output("formatted_html", type=Output.Dataset)],
                        steps=[
                            component(
                                name="display_html",
                                description="Display the formatted HTML string",
                                inputs=[Input("formatted_html", type=Input.Dataset)],
                                outputs=[
                                    Output(
                                        "mlpipeline_ui_metadata", type=Output.Dataset
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    # Define the confusion-visualization component
    confusion_visualization = component(
        name="confusion-visualization",
        description="Visualize data using confusion matrix",
        inputs=[
            Input("data", type=Input.Dataset),
            Input("thresholds", type=Input.Dataset),
        ],
        outputs=[Output("mlpipeline_ui_metadata", type=Output.Dataset)],
        steps=[
            component(
                name="generate_confusion_matrix",
                description="Generate a confusion matrix from the input dataset",
                inputs=[Input("dataset", type=Input.Dataset)],
                outputs=[Output("confusion_matrix", type=Output.Dataset)],
                steps=[
                    component(
                        name="plot_confusion_matrix",
                        description="Plot the confusion matrix",
                        inputs=[Input("confusion_matrix", type=Input.Dataset)],
                        outputs=[Output("mlpipeline_ui_metadata", type=Output.Dataset)],
                    )
                ],
            )
        ],
    )

    # Return the mlpipeline_ui_metadata output artifact
    return table_visualization.outputs["mlpipeline_ui_metadata"]
