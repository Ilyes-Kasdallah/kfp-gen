import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from kfp.components import train_test_op


@dsl.pipeline(name="TrainPlotPipeline")
def train_plot_pipeline():
    # Define the train-test operation
    train_test_op = train_test_op()

    # Define the training and plotting steps
    train_step = train_test_op.train()
    plot_step = train_test_op.plot()

    # Return the pipeline
    return train_step, plot_step


# Example usage of the pipeline
if __name__ == "__main__":
    pipeline.run(train_plot_pipeline())
