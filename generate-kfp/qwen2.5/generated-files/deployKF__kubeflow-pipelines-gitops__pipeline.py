
from kfp import dsl

@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Step 0: Get the current UTC epoch timestamp and day of the week
    step_0 = dsl.component(
        name="step_0",
        func=lambda: {
            "utc_epoch": int(dsl.now().timestamp()),
            "day_of_week": dsl.now().strftime("%A")
        }
    )

    # Step 1: Output the results of step_0
    step_1 = dsl.component(
        name="step_1",
        func=lambda: {
            "result": step_0.result()
        }
    )

    return step_1
