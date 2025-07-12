```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the upload_model component from the utils file
upload_model = load_component_from_file('utils/upload_model.yaml')

# Define the iris_model_upload pipeline
@dsl.pipeline(name='iris_model_upload')
def iris_model_upload(model):
    # Call the upload_model component with the provided model artifact
    upload_model(model=model)
```

In this solution, we first import the necessary modules from the Kubeflow Pipelines SDK. We then load the `upload_model` component from the `utils` file using `load_component_from_file`. After defining the `iris_model_upload` pipeline, we use the `@dsl.pipeline` decorator to specify the pipeline's name. Inside the pipeline definition, we call the `upload_model` component with the provided `model` artifact. This completes the Kubeflow Pipeline code for the `iris_model_upload` task.