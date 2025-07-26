
from kfp import dsl

@dsl.pipeline(name="fail-pipeline")
def fail_pipeline():
    # Execute the fail component once
    dsl.component(
        name="fail",
        python_callable=lambda: sys.exit(1),
        description="Simulates a failure operation."
    )
