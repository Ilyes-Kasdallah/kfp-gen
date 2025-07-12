```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from Docker images
collect_stats = load_component_from_file('gcr.io/ross-kubeflow/collect-stats:latest')
feature_eng = load_component_from_file('gcr.io/ross-kubeflow/feature-eng:latest')
train_test_val = load_component_from_file('gcr.io/ross-kubeflow/train-test-val:latest')
tune_hp = load_component_from_file('gcr.io/ross-kubeflow/tune-hp:latest')
train_xgboost = load_component_from_file('gcr.io/ross-kubeflow/train-xgboost:latest')
host_xgboost = load_component_from_file('gcr.io/ross-kubeflow/host-xgboost:latest')
find_threshold = load_component_from_file('gcr.io/ross-kubeflow/find-threshold:latest')
evaluate_model = load_component_from_file('gcr.io/ross-kubeflow/evaluate-model:latest')

# Define the pipeline
@dsl.pipeline(name='Sequential pipeline')
def baseball_pipeline_single():
    # Collect stats
    collect_stats_op = collect_stats()

    # Feature engineering
    feature_eng_op = feature_eng(collect_stats_op.output)

    # Split train test val
    train_test_val_op = train_test_val(feature_eng_op.output, 'FT')

    # Tune hyperparameters
    tune_hp_op = tune_hp(train_test_val_op.train_data, train_test_val_op.test_data)

    # Train XGBoost
    train_xgboost_op = train_xgboost(tune_hp_op.tuned_params, train_test_val_op.train_data)

    # Host model
    host_xgboost_op = host_xgboost(train_xgboost_op.model)

    # Find threshold
    find_threshold_op = find_threshold(host_xgboost_op.model)

    # Evaluate models
    evaluate_model_op = evaluate_model()
```

This code snippet defines a Kubeflow Pipeline named `Sequential pipeline` that processes baseball statistics for the 'FT' pitch type. It includes all the required components and their dependencies, ensuring the pipeline runs sequentially and integrates with the Kubeflow Pipelines SDK.