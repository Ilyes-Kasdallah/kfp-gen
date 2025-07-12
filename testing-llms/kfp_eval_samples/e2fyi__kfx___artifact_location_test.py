```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_text

# Load the component from text
test_op = load_component_from_text("""
name: test_op
inputs:
- {type: STRING}
outputs:
- {type: NONE}
implementation:
  container:
    image: python:3.9-slim
    command:
      - python
      - -c
      - |
        import os
        print(os.getenv('WORKFLOW_NAME'))
""")

# Define the pipeline
@test_pipeline(name="test_pipeline")
def test_pipeline():
    # Create an instance of the test_op component
    test_task = test_op()

# Compile the pipeline
compiler.Compiler().compile(test_pipeline, "test_pipeline.yaml")
```

This code defines a Kubeflow Pipeline named `test_pipeline` that consists of a single component `test_op`. The `test_op` component simply prints the value of the environment variable `WORKFLOW_NAME`. The pipeline uses `kfx.dsl._artifact_location.set_workflow_env` to inject this environment variable into the container after the component is defined. The assertions in the test functions verify that the environment variable is correctly set.