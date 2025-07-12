```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='echo-pipeline')
def echo_pipeline(
    no_default_param: int = 0,
    int_param: int = 1,
    float_param: float = 1.5,
    str_param: str = 'string_value',
    bool_param: bool = True,
    list_param: list = [1, 2, 3],
    dict_param: dict = {'key': 4}
):
    # Define the echo component
    @dsl.component
    def echo():
        return 'hello, world'

    # Execute the echo component
    echo_op = echo()

# Compile the pipeline
compiler.Compiler().compile(echo_pipeline, 'test_pipeline_parser.py')

# Run the pipeline
client = kfp.Client()
run = client.create_run_from_pipeline_package('test_pipeline_parser.py', arguments={
    'no_default_param': 0,
    'int_param': 1,
    'float_param': 1.5,
    'str_param': 'string_value',
    'bool_param': True,
    'list_param': [1, 2, 3],
    'dict_param': {'key': 4}
})
print(f'Run ID: {run.id}')
```

This code snippet defines a Kubeflow Pipeline named `echo-pipeline` with seven parameters. It includes a single component named `echo` that returns the string "hello, world". The pipeline is compiled into a Python script named `test_pipeline_parser.py` and then run using the Kubeflow Pipelines SDK.