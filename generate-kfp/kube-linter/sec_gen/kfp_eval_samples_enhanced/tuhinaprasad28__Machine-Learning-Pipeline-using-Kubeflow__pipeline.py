import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the download component
@dsl.component
def download_data(download_data_yaml):
    # Load the data from the specified YAML file
    # Example: Assuming the data is stored in a CSV file named 'data.csv'
    # Replace 'data.csv' with the actual path to your data file
    data = kfp.components.load_dataset(download_data_yaml)
    return data


# Define the first pipeline component
@dsl.pipeline(name="First Pipeline")
def first_pipeline():
    # Download the data
    data = download_data("download_data/download_data.yaml")

    # Define the model components
    @dsl.component
    def logistic_regression_model(data):
        # Split the data into features and target
        X = data.drop(columns=["target"])
        y = data["target"]

        # Train a logistic regression model
        model = kfp.components.Model(
            input=Input("X"),
            output=Output("y"),
            estimator=kfp.components.Estimator(
                model_type="LogisticRegression", params={"max_iter": 1000}
            ),
        )
        return model

    @dsl.component
    def decision_tree_model(data):
        # Split the data into features and target
        X = data.drop(columns=["target"])
        y = data["target"]

        # Train a decision tree model
        model = kfp.components.Model(
            input=Input("X"),
            output=Output("y"),
            estimator=kfp.components.Estimator(
                model_type="DecisionTreeClassifier", params={"max_depth": 10}
            ),
        )
        return model

    # Define the pipeline steps
    logistic_regression_step = logistic_regression_model(data)
    decision_tree_step = decision_tree_model(data)

    # Combine the steps into a single pipeline
    pipeline = pipeline(
        name="First Pipeline", steps=[logistic_regression_step, decision_tree_step]
    )

    # Enable caching, set retries (at least 2), and specify resource limits
    pipeline.enable_caching()
    pipeline.set_retries(2)
    pipeline.resource_limits(cpu="1", memory="1Gi")

    # Return the pipeline
    return pipeline


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(first_pipeline)
