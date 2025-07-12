```python
import kfp.dsl as dsl
from kfp.components import load_component_from_file

# Load the component from a local file
component_op = load_component_from_file('path/to/component.yaml')

# Define the first variant of the pipeline
@dsl.pipeline(name='one-step-pipeline-with-if-placeholder-supply-both')
def placeholder_if_v2(input0: str, optional_input_1: str = None, optional_input_2: str = 'default value'):
    # Execute the component with the provided inputs
    component_op(
        required_input=input0,
        optional_input_1=optional_input_1,
        optional_input_2=optional_input_2
    )

# Define the second variant of the pipeline
@dsl.pipeline(name='one-step-pipeline-with-if-placeholder-supply-none')
def placeholder_if_v2(input0: str):
    # Execute the component with the provided input
    component_op(
        required_input=input0
    )
```

In this solution, we define two variants of the pipeline using the `@dsl.pipeline` decorator. Each variant calls the `component_op` component with different sets of inputs. The `load_component_from_file` function is used to load the component from a YAML file. The `optional_input_1` and `optional_input_2` parameters are optional and have default values. The `component_op` function is executed with the provided inputs, and the outputs are simply the console output of the `echo` command within the container.