
from kfp import pipeline
from kfp.components import get_data

@dsl.pipeline(name="Docker test")
def Docker_test():
    # Load the initial dataset
    data = get_data()

    # Define the components
    classifier = get_data()
    logistic_regression = get_data()

    # Combine the components into a single pipeline
    return classifier >> logistic_regression
