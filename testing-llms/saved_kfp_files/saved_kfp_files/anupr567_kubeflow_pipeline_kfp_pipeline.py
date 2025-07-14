# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 17:11:47 2021

@author: Nikhil
"""

import kfp
from kfp import dsl


@dsl.pipeline(name='First Pipeline',
              description='Applies extraction of data and pre processing it.')
def first_pipeline():
    # Loads the yaml manifest for components
    extract_data = kfp.components.load_component_from_file('components/extract_data/extract_data.yaml')
    preprocess_data = kfp.components.load_component_from_file('components/preprocess/process_data_classifier.yaml')
    logistic_regression = kfp.components.load_component_from_file('components/logistic_regression/logistic_regression.yaml')
    random_forest_classifier = kfp.components.load_component_from_file('components/random_forest/random_forest_classifier.yaml')
    # Run task
    extract_task = extract_data()
    preprocess_task = preprocess_data(extract_task.output)
    preprocess_task.execution_options.caching_strategy.max_cache_staleness = "P0D"    # disable caching
    logistic_regression_task = linear_regression(preprocess_task.output)
    random_forest_classifier_task = random_forest_classifier(preprocess_task.output)


# submit the pipeline for execution.
# keep in mind to change the host url according to your host.
if __name__ == '__main__':
    pipeline = kfp.Client(
        host='https://4ccec0259a834495-dot-us-central1.pipelines.googleusercontent.com').create_run_from_pipeline_func(
        first_pipeline, arguments={})       
