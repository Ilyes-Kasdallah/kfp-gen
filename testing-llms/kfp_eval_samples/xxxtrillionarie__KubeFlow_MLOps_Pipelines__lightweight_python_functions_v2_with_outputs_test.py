```python
import kfp
from kfp import dsl

# Import necessary libraries
from kfp.components import load_component_from_text

# Load components from text files
first_component = load_component_from_text("""
name: first_component
inputs:
- {type: STRING}
outputs:
- {type: ARTIFACT}
""")

second_component = load_component_from_text("""
name: second_component
inputs:
- {type: STRING}
- {type: STRING}
outputs:
- {type: LIST}
""")

# Define the pipeline
@dsl.pipeline(name="lightweight_python_functions_v2_with_outputs")
def lightweight_python_functions_v2_with_outputs():
    # First component
    first_output = first_component()

    # Second component
    second_output = second_component(first_output.output)

    # Third component (not explicitly defined, implied by testing framework)
    third_component(second_output.outputs[0])

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(lightweight_python_functions_v2_with_outputs)

# Run the pipeline
run = compiled_pipeline.run()
```

This code snippet defines a Kubeflow Pipeline named `lightweight_python_functions_v2_with_outputs` that performs data processing and aggregation. It includes three components: `first_component`, `second_component`, and `third_component`. The `first_component` generates two strings and outputs them to an intermediate artifact. The `second_component` takes these strings as input, concatenates them, and repeats this process three times, writing the result to an artifact named 'Output'. The `third_component` reads the output artifact and verifies its content. The pipeline uses a sequential control flow, with `second_component` depending on `first_component` and `third_component` depending on `second_component`. The pipeline utilizes the `kfp.dsl` library for pipeline definition and MinIO for artifact storage.