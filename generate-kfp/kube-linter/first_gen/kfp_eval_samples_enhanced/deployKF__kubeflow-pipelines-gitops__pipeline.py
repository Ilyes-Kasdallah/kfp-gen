import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Step 0: Get the current UTC epoch timestamp and day of the week
    step_0 = component(
        func=lambda: {
            "utc_epoch": int(kfp.get_current_time().timestamp()),
            "day_of_week": kfp.get_current_time().strftime("%A"),
        },
        name="step_0",
    )

    # Step 1: Output the results of step_0
    step_1 = component(func=lambda: step_0, name="step_1")

    # Return the results of both steps
    return step_1


# Example usage
if __name__ == "__main__":
    my_pipeline()
