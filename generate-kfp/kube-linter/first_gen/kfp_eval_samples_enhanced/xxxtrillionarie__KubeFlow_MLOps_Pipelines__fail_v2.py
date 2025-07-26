from kfp import components
import sys


@dsl.pipeline(name="fail-pipeline")
def fail_pipeline():
    # Define the 'fail' component
    @components.component(name="fail")
    def fail():
        # Simulate a failure by exiting with a return code of 1
        sys.exit(1)


# Execute the pipeline
fail_pipeline()
