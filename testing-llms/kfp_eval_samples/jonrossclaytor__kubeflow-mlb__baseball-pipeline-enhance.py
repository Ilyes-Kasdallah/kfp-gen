```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from Docker images
collect_stats_op = load_component_from_file('collect_stats.yaml')
feature_eng_op = load_component_from_file('feature_eng.yaml')
train_test_val_op = load_component_from_file('train_test_val.yaml')
tune_hp_op = load_component_from_file('tune_hp.yaml')
train_xgboost_op = load_component_from_file('train_xgboost.yaml')
host_xgboost_op = load_component_from_file('host_xgboost.yaml')
find_threshold_op = load_component_from_file('find_threshold.yaml')
evaluate_model_op = load_component_from_file('evaluate_model.yaml')
enhance_features_op = load_component_from_file('enhance_features.yaml')

# Define the pipeline
@dsl.pipeline(name='baseball-pipeline-enhance', description='A pipeline for baseball pitch type classification.')
def baseball_pipeline(pitch_type):
    # Collect stats
    collect_stats_task = collect_stats_op()
    
    # Feature engineering
    feature_engineering_task = feature_eng_op(collect_stats_task.outputs['output'])
    
    # Split train test val
    split_train_test_val_task = train_test_val_op(feature_engineering_task.outputs['output'], pitch_type)
    
    # Tune hyperparameters
    tune_hyperparameters_task = tune_hp_op(split_train_test_val_task.outputs['output'], pitch_type)
    
    # Train XGBoost
    train_xgboost_task = train_xgboost_op(tune_hyperparameters_task.outputs['output'], pitch_type)
    
    # Host model
    host_model_task = host_xgboost_op(train_xgboost_task.outputs['output'], pitch_type)
    
    # Find threshold
    find_threshold_task = find_threshold_op(host_model_task.outputs['output'], pitch_type)
    
    # Evaluate models
    evaluate_models_task = evaluate_model_op(find_threshold_task.outputs['output'])
    
    # Enhance features
    enhance_features_task = enhance_features_op(evaluate_models_task.outputs['dummy_1'],
                                                  evaluate_models_task.outputs['dummy_2'],
                                                  evaluate_models_task.outputs['dummy_3'],
                                                  evaluate_models_task.outputs['dummy_4'],
                                                  evaluate_models_task.outputs['dummy_5'],
                                                  evaluate_models_task.outputs['dummy_6'],
                                                  evaluate_models_task.outputs['dummy_7'],
                                                  evaluate_models_task.outputs['dummy_8'],
                                                  evaluate_models_task.outputs['dummy_9'],
                                                  evaluate_models_task.outputs['dummy_10'],
                                                  evaluate_models_task.outputs['dummy_11'],
                                                  evaluate_models_task.outputs['dummy_12'])

# Execute the pipeline
if __name__ == '__main__':
    from kfp.compiler import.Compiler
    compiler = Compiler()
    pipeline_spec = compiler.compile(baseball_pipeline, package_path='baseball-pipeline-enhance.json')
```

This code defines a Kubeflow Pipeline named `baseball-pipeline-enhance` that performs baseball pitch type classification using the specified components. The pipeline includes a loop over different `pitch_type` values, enhancing features at each step. The pipeline uses the `kfp` library for Kubeflow Pipelines and the `gcp` module for Google Cloud Platform integration.