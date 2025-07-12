```python
import kfp
from kfp import dsl

# Define the Preprocess Data component
@dsl.component(
    base_image='gnovack/boston_pipeline_preprocessing:latest',
    outputs=['x_train', 'x_test', 'y_train', 'y_test']
)
def preprocess_data():
    # Placeholder for preprocessing logic
    pass

# Define the Train Model component
@dsl.component(
    base_image='gnovack/boston_pipeline_train:latest',
    inputs=['x_train', 'y_train'],
    outputs=['model']
)
def train_model(x_train, y_train):
    # Placeholder for training logic
    pass

# Define the Test Model component
@dsl.component(
    base_image='gnovack/boston_pipeline_test:latest',
    inputs=['x_test', 'y_test', 'model'],
    outputs=['mse']
)
def test_model(x_test, y_test, model):
    # Placeholder for testing logic
    pass

# Define the Deploy Model component
@dsl.component(
    base_image='gnovack/boston_pipeline_deploy_model:latest',
    inputs=['model']
)
def deploy_model(model):
    # Placeholder for deployment logic
    pass

# Define the pipeline
@dsl.pipeline(name='Boston Housing Pipeline')
def boston_housing_pipeline():
    preprocess_data_task = preprocess_data()
    
    train_model_task = train_model(preprocess_data_task.outputs['x_train'], preprocess_data_task.outputs['y_train'])
    
    test_model_task = test_model(train_model_task.outputs['x_test'], train_model_task.outputs['y_test'], train_model_task.outputs['model'])
    
    deploy_model_task = deploy_model(test_model_task.outputs['mse'])

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(boston_housing_pipeline)

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment('Boston Housing Experiment')
run = client.run(experiment.id, pipeline_name=compiled_pipeline.name, pipeline_package_path='pipeline.yaml')
```

This code snippet defines the required components and the pipeline structure using the Kubeflow Pipelines SDK. The `preprocess_data`, `train_model`, `test_model`, and `deploy_model` functions are placeholders for the actual preprocessing, training, testing, and deployment logic, respectively. The pipeline is then compiled and submitted to a Kubeflow cluster for execution.