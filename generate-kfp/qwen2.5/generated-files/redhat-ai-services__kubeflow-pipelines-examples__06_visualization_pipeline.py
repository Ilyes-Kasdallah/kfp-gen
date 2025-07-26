
from kfp import dsl

@dsl.pipeline(name="Metadata Example Pipeline")
def metadata_example_pipeline():
    # Define the components
    confusion_matrix_viz = dsl.component(
        name="confusion_matrix_viz",
        description="Generates a confusion matrix in CSV format and associated metadata for visualization within the Kubeflow UI.",
        inputs={
            "data": dsl.input(type="string"),
            "output": dsl.output(type="string")
        },
        outputs={
            "csv_output": dsl.output(type="string")
        }
    )

    # Execute the component
    confusion_matrix_viz.run(data="your_data_here", output="confusion_matrix.csv")

# Call the pipeline function
metadata_example_pipeline()
