import kfp
import my_pipeline as mykfp

# Connect to Kubeflow Pipelines cluster
client = kfp.Client( host='http://3.34.205.245:80' )
print( client.list_pipelines() )

# Specify pipeline argument values
arguments = {'a': '7', 'b': '8'}

# Create run for the addition pipeline created in my_pipeline.py
run = client.create_run_from_pipeline_func(
    mykfp.add_pipeline,
    arguments=arguments,
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
    experiment_name='my-addition-experiment'
)
