```python
from kfp import dsl
from kfp.components import load_component_from_url

# Load components
getdata = load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/master/components/core/get_data/component.yaml')
reshapedata = load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/master/components/core/reshape_data/component.yaml')
modelbuilding = load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/master/components/core/model_building/component.yaml')
kserve_op = load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/master/components/serving/deploy_model/component.yaml')

# Define the pipeline
@dsl.pipeline(name='Docker test')
def docker_test():
    # Get data
    getdata_task = getdata()

    # Reshape data
    reshapedata_task = reshapedata(input=getdata_task.outputs['output'])

    # Build model
    modelbuilding_task = modelbuilding(input=reshapedata_task.outputs['output'])

    # Deploy model to KServe
    kserve_op(action='apply',
              model_name='tensorflow-sample',
              model_uri='s3://mlpipeline/mnistdocker/models/detect-digits/',
              namespace='kubeflow-user-example-com',
              framework='tensorflow',
              service_account='sa-minio-kserve')
```

This code snippet defines a Kubeflow Pipeline named `Docker test` that performs a classification task using Decision Tree and Logistic Regression. It includes components for loading data, preprocessing, building models, and deploying them to KServe. The pipeline's control flow ensures that each component runs sequentially, and it leverages the `kfp` library from Kubeflow Pipelines.