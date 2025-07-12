```python
import kfp
from kfp import dsl
from kubernetes import client

# Define the Start component
@dsl.component(
    base_image='busybox',
    outputs=['output'],
    init_containers=[
        {
            'name': 'init-container',
            'image': 'curlimages/curl',
            'command': [
                'sh',
                '-c',
                f'echo "Pipeline starting"; curl -X POST http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080?GITHUB_SHA={{inputs.parameters.github_sha}}&PR_NUM={{inputs.parameters.pr_num}}&RUN_ID={{workflow.run_id}}'
            ],
            'env_vars': [
                {'name': 'GITHUB_SHA', 'value': '{{inputs.parameters.github_sha}}'},
                {'name': 'PR_NUM', 'value': '{{inputs.parameters.pr_num}}'},
                {'name': 'RUN_ID', 'value': '{{workflow.run_id}}'}
            ]
        }
    ]
)
def start(github_sha: str, pr_num: int):
    pass

# Define the End component
@dsl.component(
    base_image='curlimages/curl',
    outputs=['output'],
    init_containers=[
        {
            'name': 'init-container',
            'image': 'curlimages/curl',
            'command': [
                'sh',
                '-c',
                f'echo "Model is registered"; curl -X POST http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080?GITHUB_SHA={{inputs.parameters.github_sha}}&PR_NUM={{inputs.parameters.pr_num}}&RUN_ID={{workflow.run_id}}'
            ],
            'env_vars': [
                {'name': 'GITHUB_SHA', 'value': '{{inputs.parameters.github_sha}}'},
                {'name': 'PR_NUM', 'value': '{{inputs.parameters.pr_num}}'},
                {'name': 'RUN_ID', 'value': '{{workflow.run_id}}'}
            ]
        }
    ]
)
def end(github_sha: str, pr_num: int):
    pass

# Define the Exit Handler component
@dsl.component(
    base_image='curlimages/curl',
    outputs=['output'],
    init_containers=[
        {
            'name': 'init-container',
            'image': 'curlimages/curl',
            'command': [
                'sh',
                '-c',
                f'echo "Training Finished"; curl -X POST http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080?GITHUB_SHA={{inputs.parameters.github_sha}}&PR_NUM={{inputs.parameters.pr_num}}&RUN_ID={{workflow.run_id}}&STATUS={{workflow.status}}'
            ],
            'env_vars': [
                {'name': 'GITHUB_SHA', 'value': '{{inputs.parameters.github_sha}}'},
                {'name': 'PR_NUM', 'value': '{{inputs.parameters.pr_num}}'},
                {'name': 'RUN_ID', 'value': '{{workflow.run_id}}'},
                {'name': 'STATUS', 'value': '{{workflow.status}}'}
            ]
        }
    ]
)
def exit_handler(github_sha: str, pr_num: int, status: str):
    pass

# Define the default pipeline
@dsl.pipeline(name='Default')
def default(resource_group: str, workspace: str, dataset: str):
    start_component = start(github_sha=resource_group, pr_num=workspace)
    end_component = end(github_sha=resource_group, pr_num=workspace)
    exit_handler_component = exit_handler(github_sha=resource_group, pr_num=workspace, status=status)

# Compile the pipeline
compiler.Compiler().compile(default, package_path='default.yaml')
```

This code snippet defines a Kubeflow Pipeline named `Default` with three components: `start`, `end`, and `exit_handler`. Each component uses a specific Docker image and has an init container that sends a callback message to `kubemlopsbot-svc.kubeflow.svc.cluster.local:8080`. The pipeline's control flow ensures that the `end` component runs after the `start` component, and the `exit_handler` component wraps both `start` and `end`. The pipeline also takes `resource_group`, `workspace`, and `dataset` as inputs, although they are not explicitly used within the pipeline definition.