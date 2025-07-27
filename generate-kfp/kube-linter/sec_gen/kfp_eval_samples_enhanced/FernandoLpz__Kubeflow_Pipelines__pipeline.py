import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="First Pipeline")
def first_pipeline():
    # Define the download component
    @dsl.component(name="download")
    def download_data(download_data_yaml):
        # Load the dataset from the YAML file
        dataset = Dataset.from_yaml(download_data_yaml)
        return dataset

    # Define the logistic regression component
    @dsl.component(name="logistic_regression")
    def logistic_regression(dataset):
        # Train a logistic regression model on the dataset
        model = Model.from_pretrained("sklearn", "logistic_regression")
        model.fit(dataset)
        return model

    # Define the decision tree component
    @dsl.component(name="decision_tree")
    def decision_tree(model):
        # Train a decision tree model on the model
        model.fit(dataset)
        return model

    # Define the pipeline
    @dsl.pipeline(name="First Pipeline")
    def first_pipeline():
        # Download the dataset
        dataset = download_data("download_data/download_data.yaml")

        # Train logistic regression model
        logistic_regression_model = logistic_regression(dataset)

        # Train decision tree model
        decision_tree_model = decision_tree(logistic_regression_model)

        # Return the trained models
        return logistic_regression_model, decision_tree_model


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(first_pipeline)
