from kfp import components
from kfp.dsl import pipeline


@pipeline(name="parameter_value_missing")
def parameter_value_missing():
    # Define the Echo component
    @components.component(
        name="echo", description="Echoes the input text to standard output."
    )
    def echo(text):
        print(text)

    # Use the Echo component in the pipeline
    echo("Hello, World!")


# Example usage of the pipeline
if __name__ == "__main__":
    parameter_value_missing()
