```python
from kfp import dsl
from kfp.components import load_component_from_image

# Load the components from Docker images
preprocess_data = load_component_from_image('gnovack/boston_pipeline_preprocessing:latest')
train_model = load_component_from_image('gnovack/boston_pipeline_train:latest')
test_model = load_component_from_image('gnovack/boston_pipeline_test:latest')
deploy_model = load_component_from_image('gnovack/boston_pipeline_deploy_model:latest')

# Define the pipeline
@dsl.pipeline(name='Boston Housing Pipeline')
def boston_housing_pipeline():
    # Preprocess Data
    preprocess_task = preprocess_data()

    # Train Model
    train_task = train_model(preprocess_task.outputs['x_train'], preprocess_task.outputs['y_train'])

    # Test Model
    test_task = test_model(preprocess_task.outputs['x_test'], preprocess_task.outputs['y_test'], train_task.outputs['model'])

    # Deploy Model
    deploy_task = deploy_model(test_task.outputs['model'])
```

This code snippet defines a Kubeflow Pipeline named `Boston Housing Pipeline` that performs a machine learning workflow for predicting Boston housing prices. It includes four components: `Preprocess Data`, `Train Model`, `Test Model`, and `Deploy Model`. Each component is defined using the `load_component_from_image` function, which loads the corresponding Docker image into the pipeline. The pipeline is structured as a sequence of tasks, where each task depends on the previous one, ensuring that the preprocessing step is completed before training, testing, and deployment.