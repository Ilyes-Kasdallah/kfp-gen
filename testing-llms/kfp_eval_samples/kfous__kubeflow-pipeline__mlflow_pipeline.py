```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_text

# Load the mlflow_logging component from text
mlflow_logging_op = load_component_from_text("""
name: mlflow_logging_op
description: Logs parameters and metrics to an MLflow tracking server.
inputs:
- {type: STRING, description: The name of the parameter}
- {type: FLOAT, description: The accuracy of the model}
outputs:
- {type: NONE}
implementation:
  container:
    image: python:3.8-slim
    command:
      - /bin/bash
      - -c
      - |
        pip install mlflow
        mlflow.set_tracking_uri http://host.docker.internal:5000
        mlflow.start_run()
        mlflow.log_param("param", "{{inputs.param}}")
        mlflow.log_metric("accuracy", "{{inputs.accuracy}}")
        mlflow.end_run()
""")

# Define the pipeline
@dsl.pipeline(name="MLflow Logging Pipeline")
def mlflow_pipeline():
    # Execute the mlflow_logging_op component
    mlflow_logging_op(param=42, accuracy=0.95)

# Compile the pipeline into a YAML file
kfp.compiler.Compiler().compile(mlflow_pipeline, 'mlflow_pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `MLflow Logging Pipeline` that performs MLflow logging. The pipeline consists of a single component, `mlflow_logging_op`, which logs parameters and metrics to an MLflow tracking server. The pipeline is compiled into a YAML file named `mlflow_pipeline.yaml`.