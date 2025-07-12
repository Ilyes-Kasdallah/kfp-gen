```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load the components from separate files
echo_workflow_vars_op = load_component_from_file('echo_workflow_vars.yaml')
echo_podname_op = load_component_from_file('echo_podname.yaml')

# Define the pipeline
@dsl.pipeline(name='simple_pipeline')
def simple_pipeline(workflow_name):
    # Run the echo_workflow_vars component
    echo_workflow_vars_task = echo_workflow_vars_op()
    
    # Run the echo_podname component
    echo_podname_task = echo_podname_op()

# Compile the pipeline
compiler.Compiler().compile(simple_pipeline, '_artifact_location.py')
```

This code snippet defines a Kubeflow Pipeline named `simple_pipeline` that includes two components: `echo_workflow_vars` and `echo_podname`. Each component prints the corresponding environment variable. The pipeline is compiled into a Python script named `_artifact_location.py`.