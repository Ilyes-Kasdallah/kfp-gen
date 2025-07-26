
from kfp import dsl

@dsl.pipeline(name="_artifact_location_test")
def test_pipeline():
    # Define the component
    test_op = dsl.component(
        name="test_op",
        function=lambda x: print(x),
        inputs=(),
        outputs=()
    )

    # Define the pipeline
    return test_op
