import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics

# Define the pipeline root
pipeline_root = "gs://my-bucket/pipeline-root"


# Define the train-test_op component
@dsl.component
def train_test_op(url):
    # Load the test dataset from the URL
    dataset = Dataset.from_gcs(url)

    # Perform the training operation
    # Example: Assuming the training function is named 'train_model'
    trained_model = model.train_model(dataset)

    # Return the trained model
    return trained_model


# Define the train_plot_op component
@dsl.component
def train_plot_op(model):
    # Plot the trained model
    # Example: Assuming the plot function is named 'plot_model'
    plot_model(model)


# Define the TrainPlotPipeline pipeline
@dsl.pipeline(name="TrainPlotPipeline")
def train_plot_pipeline():
    # Call the train_test_op component with the URL of the test dataset
    trained_model = train_test_op(
        "https://raw.githubusercontent.com/pavan-kumar-99/ml-ops/master/components/test-train.yaml"
    )

    # Call the train_plot_op component with the trained model
    train_plot_op(trained_model)


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(train_plot_pipeline)
