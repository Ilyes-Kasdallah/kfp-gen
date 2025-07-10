#!/usr/bin/env python3

import kfp
from kfp.components import func_to_container_op, InputPath, OutputPath


read_csv = kfp.components.load_component_from_url("https://raw.githubusercontent.com/terus-lim-df/kubeflow-pipeline/main/sample1__embulk_component.yaml")


@kfp.dsl.pipeline(
  name='My pipeline',
  description='My machine learning pipeline'
)
def file_passing_pipelines(file_path):
    """Combining all pipelines together in a single pipeline"""
    read_csv(file_path)


if __name__ == '__main__':
    # Compiling the pipeline
    kfp.compiler.Compiler().compile(file_passing_pipelines, "dags/" + __file__.split("/")[-1] + '.yaml')
