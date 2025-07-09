import kfp
from kfp import dsl
import os
from components import (
    step_model_testing_catboost,
    step_hyperparam_optim_catboost,
    step_data_splitting_catboost,
    step_data_preprocessing_catboost,
)


@dsl.pipeline(
    name="Customer Frequency Training Pipeline",
    description="A kubernetes pipeline for training a customer freq prediction model",
)
def customer_freq_training_pipeline():
    data_preprocessing_task = step_data_preprocessing_catboost()
    data_splitting_task = step_data_splitting_catboost().after(data_preprocessing_task)
    hyperparam_optim_task = step_hyperparam_optim_catboost().after(data_splitting_task)
    model_testing_task = step_model_testing_catboost().after(hyperparam_optim_task)


directory_path = "compiled_pipelines/"

if not os.path.exists(directory_path):
    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except OSError as error:
        print(f"Failed to create directory '{directory_path}': {error}")
else:
    print(f"Directory '{directory_path}' already exists.")


kfp.compiler.Compiler().compile(
    pipeline_func=customer_freq_training_pipeline,
    package_path="./compiled_pipelines/Customer_freq_training_catboost.yaml",
)
