import json
from kfp import components
import kfp.dsl as dsl

@dsl.pipeline(
    name="Launch kubeflow tfjob & kfserving template",
    description="An example to launch tfjob."
)
def mnist_pipeline(
        name="mnist",
        namespace="kubeflow",
        workerNum=2,
        deleteAfterDone=False):
    tfjob_launcher_op = components.load_component_from_file("./tfJobComponent.yaml")
    bucket = "kf_second_test"
    
    chief = {}
    worker = {}
    if workerNum > 0:
      worker = {
        "replicas": 1,
        "restartPolicy": "OnFailure",
        "template": {
          "spec": {
            "terminationGracePeriodSeconds": 0,
            "containers": [
              {
                "args": [
                  "curl -s http://140.114.78.229/web/mnist-new.py | python3 -"
                ],
                "env": [
                  {
                    "name": "global_steps",
                    "value": "100000"
                  }
                ],
                "command": [
                  "/bin/bash",
                  "-c"
                ],
                "image": "ncy9371/tensorflow:1.15.2-py3-noavx",
                "name": "tensorflow",
                "ports": [
                  {
                    "containerPort": 2222,
                    "name": "tfjob-port"
                  }
                ],
                "resources": {
                  "requests": {
                    "cpu": "1",
                    "memory": "2Gi"
                  }
                }
              }
            ]
          }
        }
      }

    ps = {
        "replicas": 1,
        "restartPolicy": "OnFailure",
        "template": {
            "spec": {
            "terminationGracePeriodSeconds": 0,
            "containers": [
                {
                "args": [
                    "curl -s http://140.114.78.229/web/mnist-new.py | python3 -"
                ],
                "env": [
                    {
                    "name": "global_steps",
                    "value": "100000"
                    }
                ],
                "command": [
                    "/bin/bash",
                    "-c"
                ],
                "image": "ncy9371/tensorflow:1.15.2-py3-noavx",
                "name": "tensorflow",
                "ports": [
                    {
                    "containerPort": 2222,
                    "name": "tfjob-port"
                    }
                ]
                }
            ]
            }
        }
    }
    tfJobLauncher = tfjob_launcher_op(
      name=name,
      namespace=namespace,
      worker_spec=worker,
      chief_spec=chief,
      ps_spec=ps,
      delete_finished_tfjob=deleteAfterDone
    )

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(mnist_pipeline, __file__ + ".tar.gz")
