
from kfp import dsl

@dsl.pipeline(name="parameter_value_missing")
def parameter_value_missing():
    # Define the Echo component
    @dsl.component
    def echo(text):
        return text

    # Use the Echo component with a parameter
    result = echo("Hello, World!")

    # Return the result
    return result
