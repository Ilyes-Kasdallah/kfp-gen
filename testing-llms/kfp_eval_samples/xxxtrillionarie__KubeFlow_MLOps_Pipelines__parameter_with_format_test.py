```python
from kfp import dsl
from kfp.deprecated import components

# Importing the parameter_with_format module
import parameter_with_format

# Defining the pipeline using the @dsl.pipeline decorator
@dsl.pipeline(name='parameter_with_format_test', base_image='tensorflow/tensorflow:2.3.0')
def my_pipeline():
    # Invoking the component from the parameter_with_format module
    parameter_with_format.my_pipeline()
```

This code snippet defines a Kubeflow Pipeline named `parameter_with_format_test` that invokes the `my_pipeline` function from the `parameter_with_format` module. The pipeline uses the `V1_LEGACY` mode and does not include any parallel processing or specific control flow beyond the execution of the single component.