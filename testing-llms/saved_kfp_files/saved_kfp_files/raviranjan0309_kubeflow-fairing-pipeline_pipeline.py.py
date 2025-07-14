import kfp.dsl as dsl
import kfp.gcp as gcp
import kfp
from kubernetes.client.models import V1EnvVar
import warnings
warnings.filterwarnings('ignore')

@dsl.pipeline(
    name='Kubeflow Fairing Pipeline',
    description='Embedding Kubeflow fairing inside Kubeflow Pipeline',
)
def pipeline():
    lightgbm_train = dsl.ContainerOp(
        name='lightgbm_training',
        image='gcr.io/<GCP PROJECT ID>/lightgbm-model:latest'          
        ).apply(gcp.use_gcp_secret(secret_name='user-gcp-sa'))


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.zip')
