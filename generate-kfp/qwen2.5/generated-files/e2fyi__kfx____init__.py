
from kfp import dsl

@dsl.pipeline(name="demo")
def demo():
    # Define the echo component
    @dsl.component
    def echo(text):
        print(text)
        return text

# Example usage of the echo component
result = echo("Hello, World!")
print(result)  # Output: Hello, World!
