```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
collect_stats = load_component_from_file('components/collect_stats.yaml')
feature_engineering = load_component_from_file('components/feature_engineering.yaml')
split_train_test_val = load_component_from_file('components/split_train_test_val.yaml')
tune_hyperparameters = load_component_from_file('components/tune_hyperparameters.yaml')
train_xgboost = load_component_from_file('components/train_xgboost.yaml')
host_model = load_component_from_file('components/host_model.yaml')
find_threshold = load_component_from_file('components/find_threshold.yaml')
evaluate_models = load_component_from_file('components/evaluate_models.yaml')

# Define the pipeline
@dsl.pipeline(name='Sequential pipeline')
def baseball_pipeline():
    # Collect stats
    collect_stats_op = collect_stats()

    # Feature engineering
    feature_engineering_op = feature_engineering(collect_stats_op.output)

    # Split train test val for each pitch type
    ft_split_train_test_val = split_train_test_val(feature_engineering_op.output, pitch_type='FT')
    fs_split_train_test_val = split_train_test_val(feature_engineering_op.output, pitch_type='FS')
    ch_split_train_test_val = split_train_test_val(feature_engineering_op.output, pitch_type='CH')

    # Tune hyperparameters for each pitch type
    ft_tune_hyperparameters = tune_hyperparameters(ft_split_train_test_val.output)
    fs_tune_hyperparameters = tune_hyperparameters(fs_split_train_test_val.output)
    ch_tune_hyperparameters = tune_hyperparameters(ch_split_train_test_val.output)

    # Train XGBoost for each pitch type
    ft_train_xgboost = train_xgboost(ft_tune_hyperparameters.output)
    fs_train_xgboost = train_xgboost(fs_tune_hyperparameters.output)
    ch_train_xgboost = train_xgboost(ch_tune_hyperparameters.output)

    # Host models for each pitch type
    ft_host_model = host_model(ft_train_xgboost.output)
    fs_host_model = host_model(fs_train_xgboost.output)
    ch_host_model = host_model(ch_train_xgboost.output)

    # Find thresholds for each pitch type
    ft_find_threshold = find_threshold(ft_host_model.output)
    fs_find_threshold = find_threshold(fs_host_model.output)
    ch_find_threshold = find_threshold(ch_host_model.output)

    # Evaluate models for each pitch type
    ft_evaluate_models = evaluate_models(ft_find_threshold.output)
    fs_evaluate_models = evaluate_models(fs_find_threshold.output)
    ch_evaluate_models = evaluate_models(ch_find_threshold.output)

# Execute the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(baseball_pipeline, 'baseball-pipeline-branch.yaml')
```

This code snippet defines a Kubeflow Pipeline named `Sequential pipeline` that performs baseball pitch type classification. It includes all the required components and their dependencies, ensuring that the pipeline runs correctly with the Kubeflow Pipelines SDK.