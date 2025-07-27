import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Docker test")
def Docker_test():
    # Define the getdata component
    @component
    def getdata():
        # Load the initial dataset
        return Dataset.from_gcs("gs://my-bucket/dataset")

    # Define the logistic regression component
    @component
    def logistic_regression(input_dataset):
        # Train a logistic regression model on the dataset
        model = Model.from_kfp_model(
            "https://github.com/yourusername/yourrepo.git", "model"
        )
        metrics = Metrics()
        model.fit(input_dataset, metrics)
        return model

    # Define the decision tree component
    @component
    def decision_tree(input_dataset):
        # Train a decision tree model on the dataset
        model = Model.from_kfp_model(
            "https://github.com/yourusername/yourrepo.git", "model"
        )
        metrics = Metrics()
        model.fit(input_dataset, metrics)
        return model

    # Define the pipeline
    @dsl.pipeline
    def Docker_test():
        # Get the dataset
        dataset = getdata()

        # Train logistic regression model
        logistic_regression_output = logistic_regression(dataset)

        # Train decision tree model
        decision_tree_output = decision_tree(logistic_regression_output)

        # Return the trained models
        return logistic_regression_output, decision_tree_output


# Compile the pipeline
kfp.compiler.Compiler().compile(Docker_test)
