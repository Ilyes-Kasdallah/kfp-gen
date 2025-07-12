```python
from kfp import dsl
from kfp.components import load_component_from_text

# Load the component from text
echo_op = load_component_from_text("""
name: echo
description: A simple echo component.
inputs:
- {type: STRING, description: The message to echo}
outputs:
- {type: STRING, description: The echoed message}
implementation:
  container:
    image: alpine
    command: ["sh", "-c", "echo $0"]
""")

# Define the pipeline
@dsl.pipeline(name="echo-sh")
def my_pipeline(message: str):
    # Execute the echo component
    echo_task = echo_op(message=message)

# Compile the pipeline
kfp.compiler.Compiler().compile(my_pipeline, "echo-sh.yaml")
```

In this solution, we first load the `echo` component from text using `load_component_from_text`. We then define the `my_pipeline` function using the `@dsl.pipeline` decorator with the specified name. Inside the pipeline, we create an instance of the `echo_op` component and pass the `message` parameter to it. Finally, we compile the pipeline into a YAML file named `echo-sh.yaml` using the `kfp.compiler.Compiler()` class.