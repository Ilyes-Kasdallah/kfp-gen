from kfp import components
from kfp.dsl import pipeline


@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Define the first component
    @components.containerized
    def print_text(text):
        print(text)

    # Define the second component
    @components.containerized
    def print_text2(text):
        print(text)

    # Define the third component
    @components.containerized
    def print_text3(text):
        print(text)

    # Define the pipeline function
    @dsl.pipeline_function(after=["print_text", "print_text2", "print_text3"])
    def main():
        # Call the first component
        print_text("Hello, World!")

        # Call the second component
        print_text2("Kubeflow Pipelines!")

        # Call the third component
        print_text3("Kubernetes!")


# Run the pipeline
pipeline_with_after().execute()
