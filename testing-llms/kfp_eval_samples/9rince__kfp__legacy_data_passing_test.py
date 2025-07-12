```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the component from the file
data_passing_component = load_component_from_file('path_to_your_component.yaml')

# Define the pipeline
@dsl.pipeline(name='legacy_data_passing_pipeline')
def data_passing_pipeline():
    # Call the component
    data_passing_task = data_passing_component()

# Run the pipeline
if __name__ == '__main__':
    run_pipeline_func(data_passing_pipeline)
```

In this solution, we first load the component from the YAML file using `load_component_from_file`. Then, we define the pipeline using the `@dsl.pipeline` decorator with the specified name. Inside the pipeline, we call the loaded component using `data_passing_component()`. Finally, we run the pipeline using `run_pipeline_func(data_passing_pipeline)` if the script is executed directly.