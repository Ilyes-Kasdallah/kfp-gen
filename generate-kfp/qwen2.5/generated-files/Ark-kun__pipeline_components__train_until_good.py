
from kfp import pipeline
from kfp.components import train_until_good

@pipeline(name="train_until_low_error")
def train_until_low_error():
    # Define the training function
    train_function = train_until_good()

    # Define the graph component
    graph_component = train_function()

    # Return the graph component
    return graph_component
