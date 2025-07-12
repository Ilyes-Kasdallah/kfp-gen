```python
from kfp.deprecated import dsl
from kfp.deprecated.components import component

# Define the Echo component
@component(
    base_image='alpine',
    outputs=['output'],
    arguments=[
        '--text', '{{inputs.parameters.text}}'
    ]
)
def echo(text):
    print(text)

# Define the main pipeline
@dsl.pipeline(name='parameter_value_missing')
def fail_parameter_value_missing(parameter):
    # Call the Echo component with the provided parameter
    echo(text=parameter)

# Execute the pipeline
if __name__ == '__main__':
    from kfp.deprecated.compiler import compile_pipeline
    compile_pipeline(fail_parameter_value_missing, package_path='pipeline.yaml')
```

In this solution, we define an `Echo` component that prints the input text. We then create a main pipeline called `fail_parameter_value_missing` that calls the `Echo` component with a parameter passed through the pipeline's input. The pipeline is compiled into a YAML file named `pipeline.yaml`, which can be deployed to a Kubeflow cluster for execution.