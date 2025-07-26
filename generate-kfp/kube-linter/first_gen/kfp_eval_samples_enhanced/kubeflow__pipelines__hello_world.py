from kfp import components
from kfp.dsl import pipeline


@pipeline(name="hello-world")
def hello_world(text="hi there"):
    # Define the hello_world function
    @components.function(name="hello_world")
    def hello_world(text):
        print(text)
        return text


# Example usage of the hello_world function
result = hello_world()
print(result)  # Output: hi there
