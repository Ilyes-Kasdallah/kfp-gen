
from kfp import dsl

@dsl.pipeline(name="parameter_value_missing")
def parameter_value_missing(parameter):
    # Define the component 'Echo'
    @dsl.component(name="Echo")
    def echo(text):
        return f"Echo: {text}"

    # Use the component with the provided parameter
    result = echo(parameter)
    print(result)

# Example usage
parameter_value_missing("Hello, World!")
