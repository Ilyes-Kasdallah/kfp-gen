from kfp import components
from kfp.dsl import pipeline


@pipeline(name="fail-pipeline")
def fail_pipeline():
    # Define the 'fail' component
    @components.component(name="fail")
    def fail():
        # Simulate a failure by returning a return code of 1
        return 1


# Execute the pipeline
fail_pipeline()
