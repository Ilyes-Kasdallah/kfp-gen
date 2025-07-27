import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="lightweight_python_functions_v2_with_outputs")
def lightweight_python_functions_v2_with_outputs():
    # Define the first component
    @component(name="component_1")
    def generate_strings():
        # Generate two strings
        first_string = "first"
        second_string = "second"

        # Write the strings to separate files
        with open("output1.txt", "w") as f:
            f.write(first_string)
        with open("output2.txt", "w") as f:
            f.write(second_string)

        # Return the paths of the generated files
        return ["output1.txt", "output2.txt"]

    # Define the second component
    @component(name="component_2")
    def write_to_dataset():
        # Create a dataset
        dataset = Dataset.from_text(
            content=[
                {"name": "key1", "value": "value1"},
                {"name": "key2", "value": "value2"},
            ],
            schema={"name": "string", "type": "string"},
        )

        # Write the dataset to a file
        with open("output_dataset.csv", "w") as f:
            f.write(dataset.to_csv())

        # Return the path of the written dataset
        return "output_dataset.csv"

    # Define the third component
    @component(name="component_3")
    def write_model():
        # Create a model
        model = Model(
            name="model",
            source="https://storage.googleapis.com/my-bucket/model.tar.gz",
            version="1.0",
        )

        # Write the model to a file
        with open("output_model.tar.gz", "wb") as f:
            f.write(model.to_bytes())

        # Return the path of the written model
        return "output_model.tar.gz"


# Run the pipeline
if __name__ == "__main__":
    pipeline_root = "gs://my-bucket/pipeline-root"
    pipeline = lightweight_python_functions_v2_with_outputs()
    pipeline.run(pipeline_root=pipeline_root)
