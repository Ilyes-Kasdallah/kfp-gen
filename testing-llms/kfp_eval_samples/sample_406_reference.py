import kfp.dsl as dsl
from kfp.v2 import compiler
import kfp

from components.pythoncomponents.train import train
from components.pythoncomponents.test import test
get_model=kfp.components.load_component_from_file("components/yaml-components/get_model_component.yaml")
get_data=kfp.components.load_component_from_file("components/yaml-components/get_data_component.yaml")


@dsl.pipeline(
  name='nn-pipeline',
  description='un ejemplo de una pipeline completa de un modelo',
)
def nnpipeline():
  src = get_model(githubpath='https://github.com/javierdarksoul/src_test.git')
  data = get_data(githubpath=' https://github.com/javierdarksoul/data_test.git',folder ="FashionMNIST")
  train_task= train(src.outputs["output1path"], data.outputs["trainloader"]) 
  test(src.outputs["output1path"],train_task.outputs["weights"], data.outputs["testloader"])
  #load_task= loads(src.outputs['output1path'])

compiler.Compiler().compile(pipeline_func=nnpipeline, package_path='pipeline.json')

client = kfp.Client()
client.create_run_from_pipeline_func(
    nnpipeline,
    arguments={},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)
