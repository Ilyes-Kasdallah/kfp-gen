```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from files
check_cnt_op = load_component_from_file('path/to/check_cnt.yaml')
retrain_op = load_component_from_file('path/to/retrain.yaml')

# Define the pipeline
@dsl.pipeline(name='retrain')
def train_model(bucket_name='images-original', data_type=None):
    # Check the number of new images
    check_cnt_task = check_cnt_op(bucket_name=bucket_name)
    
    # Determine if retraining is needed
    condition = dsl.Condition(check_cnt_task.outputs['count'] > 100)
    
    # Retrain the model if necessary
    with dsl.ParallelFor(condition):
        retrain_task = retrain_op(data_dir='/path/to/training/data',
                                   model_export_dir='gs://model-cpt/')
        
        # Use a GCP service account
        gcp.use_gcp_secret("user-gcp-sa")

# Compile the pipeline
compiler.Compiler().compile(train_model, 'retrain_pipeline.json')
```

In this solution, we define the `train_model` pipeline using the `@dsl.pipeline` decorator. We load the `check_cnt` and `retrain` components from their respective YAML files using `load_component_from_file`. The pipeline includes a conditional statement that checks if the number of new images exceeds 100. If so, it executes the `retrain` component. The `retrain` component uses a GCP service account via `gcp.use_gcp_secret("user-gcp-sa")`. The pipeline is compiled into a JSON file named `retrain_pipeline.json` using the `Compiler()` class from the `kfp.compiler` module.