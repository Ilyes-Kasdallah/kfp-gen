```python
from kfp import dsl
from kfp.deprecated.components import load_component_from_text

# Load the component from text
fail_task = load_component_from_text("""
name: fail-task
description: A task that intentionally fails.
inputs:
- {type: STRING, description: Input string}
outputs:
- {type: STRING, description: Output string}
implementation:
  container:
    image: alpine:latest
    command: ["sh", "-c", "exit 1"]
""")

# Define the pipeline
@dsl.pipeline(name="fail-pipeline")
def fail():
    # Execute the fail_task component
    fail_task()
```

This code snippet defines a Kubeflow Pipeline named `fail-pipeline` that includes a single component called `fail_task`. The `fail_task` component runs an Alpine Linux container with a shell script that exits with a return code of 1, effectively failing the pipeline. The pipeline is executed without any additional components or parallel processing.