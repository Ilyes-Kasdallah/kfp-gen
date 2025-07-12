```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the component from the file
upload_model_op = load_component_from_file('upload_model.yaml')

# Define the pipeline
@dsl.pipeline(name='model_upload_pipeline')
def register(project_id: str, location: str, model: dsl.Input[dsl.Model]):
    # Execute the upload model operation
    upload_model_op(
        project_id=project_id,
        location=location,
        model=model
    )
```

In this solution, we first load the `upload_model` component from the specified YAML file using `load_component_from_file`. We then define the `register` pipeline using the `@dsl.pipeline` decorator with the provided name. Inside the pipeline, we execute the `upload_model_op` with the required parameters (`project_id`, `location`, and `model`). This completes the definition of the Kubeflow Pipeline named `model_upload_pipeline`.