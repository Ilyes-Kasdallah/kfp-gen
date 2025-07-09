import kfp
from kfp import dsl
from kfp.components import load_component_from_file

@dsl.pipeline(name="Kubeflow ML Pipeline", description="End-to-end ML pipeline")
def pipeline():
    data_load = load_component_from_file("components/data_load.py")()
    preprocess = load_component_from_file("components/preprocess.py")(data_load.output)
    train = load_component_from_file("components/train.py")(preprocess.output)
    evaluate = load_component_from_file("components/evaluate.py")(preprocess.output, train.output)
    deploy = load_component_from_file("components/deploy.py")(evaluate.output)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, 'pipeline.yaml')

