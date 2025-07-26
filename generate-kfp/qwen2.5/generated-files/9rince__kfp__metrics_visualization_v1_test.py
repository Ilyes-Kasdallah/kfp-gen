
from kfp import dsl

@dsl.pipeline(name="metrics_visualization_v1_pipeline")
def metrics_visualization_v1_pipeline():
    # Define the table visualization component
    table_visualization = dsl.component(
        name="table-visualization",
        description="Visualize metrics in a table format.",
        inputs={
            "data": dsl.input("data", type="pandas.DataFrame"),
            "columns": dsl.input("columns", type="list[str]")
        },
        outputs={
            "mlpipeline_ui_metadata": dsl.output("mlpipeline_ui_metadata", type="pandas.DataFrame")
        }
    )

    # Define the markdown visualization component
    markdown_visualization = dsl.component(
        name="markdown-visualization",
        description="Generate markdown content for metrics.",
        inputs={
            "data": dsl.input("data", type="pandas.DataFrame"),
            "columns": dsl.input("columns", type="list[str]")
        },
        outputs={
            "mlpipeline_ui_metadata": dsl.output("mlpipeline_ui_metadata", type="pandas.DataFrame")
        }
    )

    # Define the roc-visualization component
    roc_visualization = dsl.component(
        name="roc-visualization",
        description="Visualize ROC curves.",
        inputs={
            "data": dsl.input("data", type="pandas.DataFrame"),
            "columns": dsl.input("columns", type="list[str]")
        },
        outputs={
            "mlpipeline_ui_metadata": dsl.output("mlpipeline_ui_metadata", type="pandas.DataFrame")
        }
    )

    # Define the html-visualization component
    html_visualization = dsl.component(
        name="html-visualization",
        description="Generate HTML content for metrics.",
        inputs={
            "data": dsl.input("data", type="pandas.DataFrame"),
            "columns": dsl.input("columns", type="list[str]")
        },
        outputs={
            "mlpipeline_ui_metadata": dsl.output("mlpipeline_ui_metadata", type="pandas.DataFrame")
        }
    )

    # Define the confusion-visualization component
    confusion_visualization = dsl.component(
        name="confusion-visualization",
        description="Visualize confusion matrices.",
        inputs={
            "data": dsl.input("data", type="pandas.DataFrame"),
            "columns": dsl.input("columns", type="list[str]")
        },
        outputs={
            "mlpipeline_ui_metadata": dsl.output("mlpipeline_ui_metadata", type="pandas.DataFrame")
        }
    )

    # Define the metrics_visualization_test function
    metrics_visualization_test = dsl.function(
        name="metrics_visualization_test",
        description="Test the metrics_visualization_v1_pipeline function.",
        inputs={
            "data": dsl.input("data", type="pandas.DataFrame"),
            "columns": dsl.input("columns", type="list[str]")
        },
        outputs={
            "mlpipeline_ui_metadata": dsl.output("mlpipeline_ui_metadata", type="pandas.DataFrame")
        }
    )
