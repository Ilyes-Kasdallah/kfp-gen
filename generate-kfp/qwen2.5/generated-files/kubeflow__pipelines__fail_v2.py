
from kfp import pipeline, component

@pipeline(name="fail-pipeline")
def fail_pipeline():
    # Define the 'fail' component
    @component
    def fail():
        return 1

    # Execute the 'fail' component
    result = fail()
    print(f"Result of 'fail' component: {result}")
