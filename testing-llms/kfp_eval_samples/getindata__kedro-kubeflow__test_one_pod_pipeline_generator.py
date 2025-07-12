```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the component definition from a file
transform_component = load_component_from_file('path/to/your/component.yaml')

# Define the pipeline
@dsl.pipeline(name='pipeline')
def pipeline(param1: float, param2: int, param3: str):
    # Create a task that executes the transform component
    transformed_data = transform_component(
        param1=param1,
        param2=param2,
        param3=param3
    )
```

In this solution, we first load the component definition from a YAML file using `load_component_from_file`. We then define the pipeline using the `@dsl.pipeline` decorator with the specified name. Inside the pipeline, we create a task that executes the `transform_component` by passing the input parameters `param1`, `param2`, and `param3`. The output of the `transform_component` is stored in the variable `transformed_data`.