```python
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='parameter_with_format_test')
def parameter_with_format_test():
    # Define the component
    @dsl.component(
        base_image='tensorflow/tensorflow:2.10.0',
        packages_to_install=['numpy'],
        output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.DATASET)
    )
    def process_data(input_data):
        import numpy as np
        data = np.array(input_data)
        processed_data = data * 2
        return processed_data

    # Execute the component
    result = process_data(input_data=[1, 2, 3])

# Compile the pipeline
pipeline_spec = parameter_with_format_test.to_component_spec()
```

This code defines a Kubeflow Pipeline named `parameter_with_format_test` with a single component that takes an input list of numbers, multiplies each number by 2, and returns the processed data as a dataset artifact. The pipeline is compiled into a component specification which can be used to deploy the pipeline.