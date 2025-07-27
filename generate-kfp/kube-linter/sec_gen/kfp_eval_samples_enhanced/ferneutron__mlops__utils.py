import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the utils function as the pipeline function name
@dsl.pipeline(name="iris_model_upload")
def upload_model(model_path: str) -> Output[Model]:
    # Load the model from the provided path
    model = Model.from_file(model_path)

    # Upload the model to Vertex AI
    # Note: This is a placeholder for actual Vertex AI API calls
    # Replace with actual Vertex AI API calls
    # For example, you might use the following code:
    # from google.cloud import vertexai
    # client = vertexai.Client()
    # model = client.models.create(
    #     parent="projects/your-project-id",
    #     model=model_path,
    #     display_name="Your Model Name"
    # )
    # return model
