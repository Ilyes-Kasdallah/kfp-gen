from kfp import components
from kfp.dsl import pipeline


@pipeline(name="parameter_value_missing")
def parameter_value_missing(parameter):
    # Define the Echo component
    @components.component(
        name="Echo",
        image="alpine",
        command=["echo", parameter],
    )
    def echo(text):
        return text

    # Use the Echo component in the pipeline
    echo_result = echo(parameter)
    print(echo_result)


# Example usage
if __name__ == "__main__":
    parameter_value_missing("Hello, World!")
