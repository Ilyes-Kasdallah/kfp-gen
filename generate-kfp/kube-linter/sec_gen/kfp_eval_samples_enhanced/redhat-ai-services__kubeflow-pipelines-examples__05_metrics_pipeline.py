import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="metrics pipeline")
def produce_metrics(
    input_dataset: Dataset,
    output_accuracy_score: Output[Metrics],
    output_mse_score: Output[Metrics],
):
    # Generate accuracy score
    accuracy_score = input_dataset.read_csv().mean()

    # Generate mse score
    mse_score = input_dataset.read_csv().variance()

    # Store results in the output
    output_accuracy_score.set_value(accuracy_score)
    output_mse_score.set_value(mse_score)


# Example usage of the pipeline function
if __name__ == "__main__":
    # Define the input dataset
    input_dataset = Dataset.from_gcs("gs://my-bucket/input_dataset.csv")

    # Call the produce_metrics function
    produce_metrics(
        input_dataset=input_dataset,
        output_accuracy_score=output_accuracy_score,
        output_mse_score=output_mse_score,
    )
