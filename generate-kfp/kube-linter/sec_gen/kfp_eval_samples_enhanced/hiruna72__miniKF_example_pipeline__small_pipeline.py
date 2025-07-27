import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the small_pipeline function
@dsl.pipeline(name="small_pipeline")
def small_pipeline(
    input_file: Input[Dataset], multiplier: float, output_uri: Output[Model]
):
    # Load the input file into a dataset
    dataset = Dataset.from_gcs(input_file)

    # Multiply the dataset by the multiplier
    multiplied_dataset = dataset.multiply(multiplier)

    # Save the result to the specified output URI
    multiplied_dataset.save(output_uri)


# Example usage of the small_pipeline function
if __name__ == "__main__":
    small_pipeline()
