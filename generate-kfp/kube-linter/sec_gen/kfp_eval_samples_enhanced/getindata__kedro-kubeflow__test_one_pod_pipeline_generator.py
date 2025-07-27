import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="pipeline")
def test_one_pod_pipeline_generator(param1: float, param2: int, param3: str):
    # Define the first component
    @component
    def transform_data(input_dataset: Dataset[str]) -> Dataset[str]:
        # Perform data transformation here
        transformed_data = input_dataset.map(lambda x: f"{x} processed")
        return transformed_data

    # Define the second component
    @component
    def process_output(output_dataset: Dataset[str]) -> Dataset[str]:
        # Process the output data here
        processed_output = output_dataset.filter(lambda x: x.startswith("processed"))
        return processed_output

    # Define the pipeline
    @pipeline
    def pipeline():
        # Use the first component to transform data
        transformed_data = transform_data(input_dataset="input_data.csv")

        # Use the second component to process the transformed data
        processed_output = process_output(transformed_data)

        # Return the processed output
        return processed_output


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(pipeline)

# Print the compiled pipeline
print(compiled_pipeline)
