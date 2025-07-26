from kfp import components
from kfp.dsl import pipeline

# Define a Kubeflow client
client = components.Client()


# Define a pipeline function
@pipeline(name="test_kfpclient")
def test_kfpclient():
    # Example Kubeflow step
    result = client.invoke("echo", "Hello, Kubeflow!")
    print(result)


# Run the pipeline
test_kfpclient()
