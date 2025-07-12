```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from Docker images
preprocess_data_op = load_component_from_file('path/to/preprocess_data.yaml')
train_model_op = load_component_from_file('path/to/train_model.yaml')
test_model_op = load_component_from_file('path/to/test_model.yaml')
deploy_model_op = load_component_from_file('path/to/deploy_model.yaml')

# Define the pipeline
@dsl.pipeline(name='Pipeline')
def pipeline():
    # Preprocess data
    preprocess_data_task = preprocess_data_op()

    # Train model
    train_model_task = train_model_op(preprocess_data_task.outputs['x_train'], preprocess_data_task.outputs['y_train'])

    # Test model
    test_model_task = test_model_op(train_model_task.outputs['x_test'], train_model_task.outputs['y_test'], train_model_task.outputs['model'])

    # Deploy model
    deploy_model_task = deploy_model_op(test_model_task.outputs['model'])
```

In this solution, we define a Kubeflow Pipeline named `Pipeline` using the `@dsl.pipeline` decorator. We load the components from Docker images using `load_component_from_file` and define the pipeline by chaining these components together. Each component is executed sequentially, and the outputs of one component are consumed by the next. The pipeline is then compiled into a YAML file for deployment to Kubeflow.