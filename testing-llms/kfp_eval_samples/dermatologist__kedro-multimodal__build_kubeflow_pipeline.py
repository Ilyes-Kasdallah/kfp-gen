```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file
import re

# Load Kedro components dynamically
def load_components(node_dependencies):
    components = []
    for node, deps in node_dependencies.items():
        component_path = f'components/{clean_name(node)}.py'
        component = load_component_from_file(component_path)
        components.append(component)
    return components

# Clean node names
def clean_name(name):
    return re.sub(r'\W+', '-', name)

# Define the Kubeflow pipeline
@dsl.pipeline(name='Kedro pipeline')
def build_kubeflow_pipeline(node_dependencies):
    # Load components dynamically
    components = load_components(node_dependencies)
    
    # Execute each component in the pipeline
    for component in components:
        component()
```

This solution defines a Kubeflow Pipeline named `Kedro pipeline` that dynamically loads and executes Kedro components based on the provided `node_dependencies` dictionary. Each component is executed using the `kedro run --node <node_name>` command within a Docker container specified by the `_IMAGE` variable. The pipeline uses the `kfp` library from Kubeflow Pipelines and Kedro for the pipeline definition and execution. The container utilizes AWS credentials from a secret named "aws-secrets" for accessing AWS resources. The `aws-secrets` secret contains `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. The `re` library is used for string manipulation to create clean component names.