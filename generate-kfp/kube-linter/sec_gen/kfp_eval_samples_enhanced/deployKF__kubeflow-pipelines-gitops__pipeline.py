import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="my_pipeline")
def my_pipeline():
    # Step 0: Get the current UTC epoch timestamp and day of the week
    utc_epoch = int(kfp.get_current_time().timestamp())
    day_of_week = kfp.get_current_time().strftime("%A")

    # Step 1: Output a named tuple containing utc_epoch and day_of_week
    return Output(name="utc_epoch_day_of_week", value=(utc_epoch, day_of_week))


# Example usage of the pipeline function
if __name__ == "__main__":
    # Run the pipeline
    my_pipeline()
