
from kfp import pipeline
from kfp.components import component

# Define a Kubeflow client
client = pipeline.Client()

# Define a pipeline function
@dsl.pipeline(name='test_kfpclient')
def test_kfpclient():
    # Define a component that performs some operation
    @component
    def perform_operation(x):
        return x * 2

    # Use the component in the pipeline
    result = perform_operation(5)
    print(result)

# Run the pipeline
test_kfpclient()
