```python
from kfp import dsl
from kfp.components import load_component_from_docker

# Load the components from Docker images
check_files_op = load_component_from_docker('tseo/check_bucket:0.3')
move_files_op = load_component_from_docker('tseo/mv_files:0.6')

# Define the pipeline
@dsl.pipeline(name='viai-retrain')
def viai_retrain():
    # Step 1: Check files
    check_files_task = check_files_op()
    
    # Step 2: Move files
    move_files_task = move_files_op(json_file=check_files_task.outputs['file_num'])

# Execute the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(viai_retrain, 'pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `viai-retrain` with two steps: checking the existence and number of files in a specified location and moving files based on the information provided in the JSON file. The pipeline uses the Kubeflow Pipelines SDK to define the components and their dependencies.