```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from files
upload_data_op = load_component_from_file('upload_data.yaml')
preprocess_op = load_component_from_file('preprocess.yaml')
split_data_op = load_component_from_file('split_data.yaml')
train_model_op = load_component_from_file('train_model.yaml')  # Assuming this component exists
evaluate_model_op = load_component_from_file('evaluate_model.yaml')  # Assuming this component exists
print_best_model_op = load_component_from_file('print_best_model.yaml')  # Assuming this component exists

@dsl.pipeline(name='MyKubeflowPipeline')
def my_kubeflow_pipeline(
    dataset_name: str,
    dataset_subset: str,
    model_name: str,
):
    # Upload dataset
    upload_data_task = upload_data_op(dataset_name=dataset_name, dataset_subset=dataset_subset)

    # Preprocess dataset
    preprocess_task = preprocess_op(dataset_object=upload_data_task.outputs['dataset'], model_name=model_name)

    # Split dataset
    split_data_task = split_data_op(dataset_object=preprocess_task.outputs['dataset'])

    # Train model
    train_model_task = train_model_op(training_dataset=split_data_task.outputs['training_dataset'],
                                      validation_dataset=split_data_task.outputs['validation_dataset'])

    # Evaluate model
    evaluate_model_task = evaluate_model_op(trained_model=train_model_task.outputs['trained_model'],
                                          test_dataset=split_data_task.outputs['test_dataset'])

    # Print best model
    print_best_model_task = print_best_model_op(evaluation_metrics=evaluate_model_task.outputs['evaluation_metrics'])
```

This code defines a Kubeflow Pipeline named `MyKubeflowPipeline` that includes all the required components and their dependencies. Each component is defined using the `load_component_from_file` function, which loads the component definitions from YAML files. The pipeline's control flow is sequential, with each component executing after the successful completion of its preceding component.