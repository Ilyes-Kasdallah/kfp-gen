```python
from kfp import dsl

# Define the echo component
@dsl.component(
    output_artifact=dsl.OutputArtifact(type=dsl.String)
)
def echo(no_default_param: int = 0,
         int_param: int = 1,
         float_param: float = 1.5,
         str_param: str = "string_value",
         bool_param: bool = True,
         list_param: list = [1, 2, 3],
         dict_param: dict = {"key": 4}
) -> str:
    return f"hello, world"

# Define the pipeline
@dsl.pipeline(name="echo-pipeline")
def test_pipelines():
    # Call the echo component
    echo_task = echo()

# Compile the pipeline
compiler.Compiler().compile(test_pipelines, 'test_pipelines.yaml')
```

This code snippet defines a Kubeflow Pipeline named `echo-pipeline` with a single component `echo`. The `echo` component takes various parameters and returns a string "hello, world". The pipeline is compiled into a YAML file named `test_pipelines.yaml`.