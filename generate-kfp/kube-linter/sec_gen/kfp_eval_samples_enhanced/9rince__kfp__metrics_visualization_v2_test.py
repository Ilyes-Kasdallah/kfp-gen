import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_v2_test():
    # Step 1: Wine Classification
    wine_classification = component(
        name="wine-classification",
        inputs={
            "data": Input(Dataset("wine_data.csv")),
        },
        outputs={
            "metrics": Output(Metrics()),
        },
        steps=[
            {
                "name": "load_data",
                "inputs": {
                    "data": Input(Dataset("wine_data.csv")),
                },
                "outputs": {
                    "data": Output(Dataset("wine_data_cleaned.csv")),
                },
            },
            {
                "name": "train_model",
                "inputs": {
                    "data": Input(Dataset("wine_data_cleaned.csv")),
                },
                "outputs": {
                    "model": Output(Model("wine_model")),
                },
            },
            {
                "name": "evaluate_model",
                "inputs": {
                    "model": Input(Model("wine_model")),
                },
                "outputs": {
                    "metrics": Output(Metrics()),
                },
            },
        ],
    )

    # Step 2: Visualize Metrics
    visualize_metrics = component(
        name="visualize_metrics",
        inputs={
            "model": Input(Model("wine_model")),
        },
        outputs={
            "visualization": Output(Dataset("wine_metrics.png")),
        },
        steps=[
            {
                "name": "generate_report",
                "inputs": {
                    "model": Input(Model("wine_model")),
                },
                "outputs": {
                    "report": Output(Dataset("wine_report.pdf")),
                },
            },
        ],
    )

    # Step 3: Combine Metrics and Visualization
    combine_metrics_and_visualization = component(
        name="combine_metrics_and_visualization",
        inputs={
            "metrics": Input(Metrics()),
            "visualization": Input(Dataset("wine_metrics.png")),
        },
        outputs={
            "combined_metrics": Output(Metrics()),
        },
        steps=[
            {
                "name": "display_results",
                "inputs": {
                    "combined_metrics": Input(Metrics()),
                },
                "outputs": {
                    "display": Output(Dataset("wine_display.pdf")),
                },
            },
        ],
    )

    # Step 4: Save Results
    save_results = component(
        name="save_results",
        inputs={
            "combined_metrics": Input(Metrics()),
            "output_dir": Output(Directory("results")),
        },
        outputs={
            "saved_results": Output(Dataset("wine_results.csv")),
        },
        steps=[
            {
                "name": "upload_results",
                "inputs": {
                    "combined_metrics": Input(Metrics()),
                    "output_dir": Output(Directory("results")),
                },
                "outputs": {
                    "uploaded_results": Output(Dataset("wine_results.csv")),
                },
            },
        ],
    )

    # Step 5: Run the pipeline
    return (
        wine_classification
        + visualize_metrics
        + combine_metrics_and_visualization
        + save_results
    )
