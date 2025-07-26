
from kfp import dsl

@dsl.pipeline(name="TrainPlotPipeline")
def train_plot_pipeline():
    # Load the train-test component from the URL
    train_test_op = dsl.component(
        "test-train.yaml",
        description="Load and preprocess the training data"
    )

    # Define the training and plotting steps
    train_op = train_test_op()
    plot_op = dsl.component(
        "plot-train.yaml",
        description="Plot the training results"
    )

    # Combine the training and plotting steps into a single pipeline function
    return train_op >> plot_op
