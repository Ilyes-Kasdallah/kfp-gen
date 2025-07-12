```python
from kfp import dsl
from kfp.components import load_component_from_text

# Load the print_all_placeholders component from text
print_all_placeholders_op = load_component_from_text("""
apiVersion: kubeflow.org/v2alpha1
kind: Component
metadata:
  name: print_all_placeholders
spec:
  implementation:
    container:
      image: python:3.8-slim
      command:
        - /bin/bash
        - -c
        - |
          echo "$1,$2,$3,$4,$5"
      args:
        - ${{inputs.parameters.job_name}}
        - ${{inputs.parameters.job_resource_name}}
        - ${{inputs.parameters.job_id}}
        - ${{inputs.parameters.task_name}}
        - ${{inputs.parameters.task_id}}
""")

# Define the pipeline with a single component
@dsl.pipeline(name="pipeline-with-placeholders")
def pipeline_with_placeholders(
    job_name: str,
    job_resource_name: str,
    job_id: str,
    task_name: str,
    task_id: str
):
    # Execute the print_all_placeholders component
    print_all_placeholders_op(job_name=job_name, job_resource_name=job_resource_name, job_id=job_id, task_name=task_name, task_id=task_id)
```

This code snippet defines a Kubeflow Pipeline named `pipeline-with-placeholders` that includes a single component `print_all_placeholders`. The component takes five string parameters and prints them out. The pipeline is executed with the specified parameters.