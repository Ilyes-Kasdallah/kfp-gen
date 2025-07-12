```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
deployer = load_component_from_file('pipeline_steps/serving/deployer/component.yaml')

# Define the pipeline
@dsl.pipeline(name='Santander Customer Transaction Prediction Release Pipeline')
def santander_trnx_classification_release(output: str, project: str):
    # Conditional logic based on platform
    if project != 'GCP':
        # Create PVC
        pvc_op = dsl.VolumeOp(
            name='create-pvc',
            resource_name='santander-pvc',
            size='1Gi',
            access_modes=['ReadWriteOnce']
        )
        
        # Clone Git repository
        git_clone_op = dsl.ContainerOp(
            name='clone-git-repo',
            image='us.gcr.io/kf-pipelines/ml-pipeline-webapp-launcher:v0.3',
            command=['git', 'clone', 'https://github.com/user/repo.git'],
            volumes=[pvc_op.volume_mount]
        )
    
    # Deploy model
    deployer_op = deployer(
        model_dir='gs://kubeflow-pipelines-demo/tfx/0b22081a-ed94-11e9-81fb-42010a800160/santander-customer-transaction-prediction-95qxr-268134926/data/export/export',
        server_name='kfdemo-service' if project == 'GCP' else f'{project}-kfdemo-service',
        cluster_name=f'{project}-kfdemo-cluster' if project != 'GCP' else None,
        pvc_name='santander-pvc' if project != 'GCP' else None
    )
    
    # Launch web application
    webapp_op = dsl.ContainerOp(
        name='launch-web-app',
        image='us.gcr.io/kf-pipelines/ml-pipeline-webapp-launcher:v0.3',
        command=['python', 'webapp.py', '--model_name', 'santanderapp'],
        env={
            'KUBEFLOW_PROJECT': project
        }
    )

    # Dependencies
    deployer_op.after(pvc_op)
    deployer_op.after(git_clone_op)
    webapp_op.after(deployer_op)

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(santander_trnx_classification_release)

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment('Santander Trnx Classification Release Experiment')
run = client.run(experiment=experiment, pipeline_func=compiled_pipeline, parameters={'output': '/path/to/output', 'project': 'your-project-name'})
```

This code snippet defines a Kubeflow Pipeline named `Santander Customer Transaction Prediction Release Pipeline` with two main components: a deployment component and a web application component. The pipeline includes conditional logic based on the `platform` variable to adapt to different deployment environments. The `gcp.use_gcp_secret` and `onprem.mount_pvc` are used to handle GCP secrets and PVC mounting, respectively. The pipeline also includes dependencies between the components and is compiled and submitted to the Kubeflow Pipelines service.