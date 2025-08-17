from kfp import dsl
from kfp.gcp import use_gcp_secret

@dsl.component(base_image='gcr.io/ross-kubeflow/collect-stats:latest')
def collect_stats():
    pass

@dsl.component(base_image='gcr.io/ross-kubeflow/feature-eng:latest')
def feature_engineering(pitch_type: str):
    pass

@dsl.component(base_image='gcr.io/ross-kubeflow/train-test-val:latest')
def split_train_test_val(pitch_type: str):
    pass

@dsl.component(base_image='gcr.io/ross-kubeflow/tune-hp:latest')
def tune_hyperparameters(pitch_type: str):
    pass

@dsl.component(base_image='gcr.io/ross-kubeflow/train-xgboost:latest')
def train_xgboost(pitch_type: str):
    pass

@dsl.component(base_image='gcr.io/ross-kubeflow/host-xgboost:latest')
def host_model(pitch_type: str):
    pass

@dsl.component(base_image='gcr.io/ross-kubeflow/find-threshold:latest')
def find_threshold(pitch_type: str):
    pass

@dsl.component(base_image='gcr.io/ross-kubeflow/evaluate-model:latest')
def evaluate_models(pitch_type: str, dummy1: str = ''):
    return dsl.OutputPath('/root/dummy.txt')

@dsl.pipeline(name='Sequential pipeline')
def sequential_pipeline(pitch_type: str):
    collect_stats_task = collect_stats()
    feature_engineering_task = feature_engineering(pitch_type=pitch_type).after(collect_stats_task)
    split_train_test_val_task = split_train_test_val(pitch_type=pitch_type).after(feature_engineering_task)
    tune_hyperparameters_task = tune_hyperparameters(pitch_type=pitch_type).after(split_train_test_val_task)
    train_xgboost_task = train_xgboost(pitch_type=pitch_type).after(tune_hyperparameters_task)
    host_model_task = host_model(pitch_type=pitch_type).after(train_xgboost_task)
    find_threshold_task = find_threshold(pitch_type=pitch_type).after(host_model_task)
    evaluate_models_task = evaluate_models(pitch_type=pitch_type, dummy1='').after(find_threshold_task)