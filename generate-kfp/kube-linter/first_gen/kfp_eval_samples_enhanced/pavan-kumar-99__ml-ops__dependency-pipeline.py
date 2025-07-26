from kfp import pipeline, component


@dsl.pipeline(name="my-pipeline")
def my_pipeline():
    # Define the first component: echo
    @component
    def echo():
        return "Hi Kubeflow"

    # Define the second component: echo
    @component
    def echo():
        return "Hello World"

    # Define the dependency between the two components
    @dsl.pipeline.function(name="dependency-pipeline")
    def dependency_pipeline():
        # Use the echo component as a dependency
        result = echo()
        print(result)


# Run the pipeline
dependency_pipeline()
