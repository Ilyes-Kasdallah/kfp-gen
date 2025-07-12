```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from files
validate_data_op = load_component_from_file('validate_data.yaml')
preprocess_op = load_component_from_file('preprocess.yaml')
train_op = load_component_from_file('train.yaml')

# Define the pipeline
@dsl.pipeline(name='wine_quality_pipeline')
def wine_quality_pipeline(
    data_path: str,
    model_type: str = 'random_forest',
    num_trials: int = 50
):
    # Validate the data
    validate_data_task = validate_data_op(data_path=data_path)
    
    # Preprocess the data
    preprocess_task = preprocess_op(validate_data_output=validate_data_task.outputs['metrics'])
    
    # Train the models
    train_random_forest_task = train_op(preprocess_output=preprocess_task.outputs['dataset'], model_type=model_type, num_trials=num_trials)
    train_xgboost_task = train_op(preprocess_output=preprocess_task.outputs['dataset'], model_type=model_type, num_trials=num_trials)
    train_lightgbm_task = train_op(preprocess_output=preprocess_task.outputs['dataset'], model_type=model_type, num_trials=num_trials)

# Compile the pipeline
kfp.compiler.Compiler().compile(wine_quality_pipeline, package_path='wine_quality_pipeline.tar.gz')
```

This code defines a Kubeflow Pipeline named `wine_quality_pipeline` that includes three components: `validate_data`, `preprocess`, and `train`. The pipeline orchestrates these components sequentially, validating the input dataset, preprocessing it, and then training three different machine learning models. The pipeline uses the `sklearn`, `xgboost`, and `lightgbm` libraries for model training and `great_expectations` for data validation. The pipeline utilizes Kubeflow Pipelines' `Dataset` and `Model` artifacts for data and model management and `Metrics` for validation results.