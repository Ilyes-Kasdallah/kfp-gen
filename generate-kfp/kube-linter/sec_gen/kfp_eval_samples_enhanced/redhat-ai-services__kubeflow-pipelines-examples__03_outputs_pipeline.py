import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="Submitted Pipeline")
def Submitted_Pipeline():
    # Define the first component
    @component(
        name="return_multiple_values",
        description="Returns a tuple containing the sum and product of two float inputs.",
        inputs=[Input("a", dtype=float), Input("b", dtype=float)],
        outputs={"sum": Output(float), "product": Output(float)},
    )
    def return_multiple_values(a, b):
        return {"sum": a + b, "product": a * b}

    # Define the second component
    @component(
        name="process_data",
        description="Processes the input data by squaring it.",
        inputs=[Input("data", dtype=Dataset)],
        outputs={"processed_data": Output(Dataset)},
    )
    def process_data(data):
        processed_data = data.map(lambda x: x**2)
        return processed_data

    # Define the pipeline root
    pipeline_root = "gs://my-bucket/pipeline-root"

    # Execute the pipeline
    Submitted_Pipeline()
