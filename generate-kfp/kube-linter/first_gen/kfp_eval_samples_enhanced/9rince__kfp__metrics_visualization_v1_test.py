import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from kfp.components import (
    table_visualization,
    markdown_visualization,
    roc_visualization,
    html_visualization,
    confusion_visualization,
)


@dsl.pipeline(name="metrics_visualization_v1_pipeline")
def metrics_visualization_v1_pipeline():
    # Define the table visualization component
    table_visualization_component = table_visualization()

    # Define the markdown visualization component
    markdown_visualization_component = markdown_visualization()

    # Define the roc visualization component
    roc_visualization_component = roc_visualization()

    # Define the html visualization component
    html_visualization_component = html_visualization()

    # Define the confusion visualization component
    confusion_visualization_component = confusion_visualization()

    # Define the pipeline UI metadata component
    mlpipeline_ui_metadata_component = table_visualization_component.output

    # Return the pipeline UI metadata component
    return mlpipeline_ui_metadata_component


# Example usage of the pipeline function
if __name__ == "__main__":
    metrics_visualization_v1_pipeline()
