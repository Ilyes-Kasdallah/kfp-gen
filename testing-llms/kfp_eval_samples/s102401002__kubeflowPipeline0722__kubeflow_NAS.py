```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
load_data_op = load_component_from_file('load_data.yaml')
prepare_data_op = load_component_from_file('prepare_data.yaml')

# Define the pipeline
@dsl.pipeline(name='DiabetesPredictionPipeline')
def diabetes_prediction_pipeline(nas_mount_path):
    # Load data
    load_data_task = load_data_op(nas_mount_path=nas_mount_path)
    
    # Prepare data
    prepare_data_task = prepare_data_op(input_artifact=load_data_task.outputs['output'])
```

In this solution, we define a Kubeflow Pipeline named `DiabetesPredictionPipeline` using the `@dsl.pipeline` decorator. We load the `load_data` and `prepare_data` components from YAML files using `load_component_from_file`. The `diabetes_prediction_pipeline` function orchestrates the execution of these components sequentially. The `load_data_task` loads the data from the specified NAS mount path, and the `prepare_data_task` processes the loaded data, splitting it into training and testing sets.