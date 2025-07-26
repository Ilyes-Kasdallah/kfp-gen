from kfp import pipeline
from kfp.dsl import component


@component
def echo(text):
    """Echoes the given text to the standard output."""
    print(text)
    return text


@pipeline(name="demo")
def demo():
    """Runs the demo pipeline."""
    # Define the first component
    echo_component = echo("Hello, World!")

    # Define the second component
    visualization_component = echo("Visualization of the text echo.")

    # Combine the components into a single pipeline
    return echo_component + visualization_component


# Run the pipeline
demo()
