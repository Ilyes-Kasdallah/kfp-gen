from kfp import components
from kfp.dsl import pipeline


@pipeline(name="two-step-with-uri-placeholder")
def two_step_with_uri_placeholder():
    # Define the first step
    @components.component(
        name="step1",
        description="This is the first step of the pipeline.",
        inputs={
            "uri": components.uri("https://example.com/data.csv"),
        },
        outputs={
            "output": components.output(),
        },
    )
    def step1(uri):
        # Simulate some processing
        print(f"Processing data from {uri}")
        return f"Processed data from {uri}"

    # Define the second step
    @components.component(
        name="step2",
        description="This is the second step of the pipeline.",
        inputs={
            "input": components.input(),
        },
        outputs={
            "output": components.output(),
        },
    )
    def step2(input):
        # Simulate some processing
        print(f"Processing input {input}")
        return f"Processed input {input}"

    # Execute both steps
    result1 = step1("https://example.com/data.csv")
    result2 = step2(result1)

    # Return the results
    return result1, result2


# Example usage
if __name__ == "__main__":
    result1, result2 = two_step_with_uri_placeholder()
    print(f"Result 1: {result1}")
    print(f"Result 2: {result2}")
