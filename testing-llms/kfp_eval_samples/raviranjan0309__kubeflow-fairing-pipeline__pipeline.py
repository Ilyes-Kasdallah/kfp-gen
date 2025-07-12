```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the component from a local file
lightgbm_training_op = load_component_from_file('path/to/lightgbm_training.yaml')

# Define the pipeline
@dsl.pipeline(name='Kubeflow Fairing Pipeline')
def lightgbm_pipeline():
    # Call the component
    lightgbm_training_task = lightgbm_training_op()
```

In this solution, we first import the necessary modules from the Kubeflow Pipelines SDK. We then load the component from a YAML file using `load_component_from_file`. After defining the pipeline, we use the `@dsl.pipeline` decorator to specify the pipeline's name. Inside the pipeline, we call the `lightgbm_training_op` component, which represents the training process. This setup ensures that the pipeline can be executed using the Kubeflow Pipelines SDK, leveraging the specified Docker image and component for training a LightGBM model.