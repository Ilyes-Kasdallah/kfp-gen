```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the components from files
data_volume_create = load_component_from_file('path/to/data_volume_create.component.yaml')
data_volume_init = load_component_from_file('path/to/data_volume_init.component.yaml')
node1 = load_component_from_file('path/to/node1.component.yaml')
node2 = load_component_from_file('path/to/node2.component.yaml')
node3 = load_component_from_file('path/to/node3.component.yaml')  # Placeholder
node4 = load_component_from_file('path/to/node4.component.yaml')  # Placeholder
node5 = load_component_from_file('path/to/node5.component.yaml')  # Placeholder
on_exit = load_component_from_file('path/to/on_exit.component.yaml')

# Define the pipeline
@dsl.pipeline(name='pipeline')
def test_pod_per_node_pipeline_generator():
    # Create the data volume
    data_volume_pvc = data_volume_create()

    # Initialize the data volume
    initialized_data_volume = data_volume_init(data_volume_pvc)

    # Process data in node1
    processed_data_node1 = node1(initialized_data_volume)

    # Process data in node2
    processed_data_node2 = node2(processed_data_node1)

    # Process data in node3
    processed_data_node3 = node3(processed_data_node2)

    # Process data in node4
    processed_data_node4 = node4(processed_data_node3)

    # Process data in node5
    processed_data_node5 = node5(processed_data_node4)

    # Delete the data volume after processing
    on_exit(processed_data_node5)
```

In this solution, we define the pipeline using the `@dsl.pipeline` decorator with the specified name. We load the components from YAML files using `load_component_from_file` and define each component as a separate function. The pipeline orchestrates the execution of these components in sequence, ensuring that the data volume is properly managed throughout the process.