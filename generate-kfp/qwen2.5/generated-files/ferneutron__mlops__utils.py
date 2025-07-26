
from kfp import components
from kfp import dsl

@dsl.pipeline(name="iris_model_upload")
def iris_model_upload(model_path):
    # Upload the model to Vertex AI
    upload_model = components.load_component("upload_model")
    upload_model.model = model_path
    return upload_model
