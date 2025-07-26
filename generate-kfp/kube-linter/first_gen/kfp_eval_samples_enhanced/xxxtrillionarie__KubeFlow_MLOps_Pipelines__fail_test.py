from kfp import components
from kfp.dsl import pipeline


@pipeline(name="fail_pipeline")
def fail_pipeline():
    # Define the first version of the pipeline using the V1 legacy engine
    @components.component(
        name="fail_v1",
        description="A simple failure test using the V1 legacy engine.",
        inputs=(),
        outputs=(),
    )
    def fail_v1():
        raise ValueError("This is a test failure.")

    # Define the second version of the pipeline using the V2 engine
    @components.component(
        name="fail_v2",
        description="A simple failure test using the V2 engine.",
        inputs=(),
        outputs=(),
    )
    def fail_v2():
        raise ValueError("This is another test failure.")

    # Combine the two versions into a single pipeline
    return fail_v1() | fail_v2()


# Example usage of the pipeline
if __name__ == "__main__":
    result = fail_pipeline()
    print(result)
