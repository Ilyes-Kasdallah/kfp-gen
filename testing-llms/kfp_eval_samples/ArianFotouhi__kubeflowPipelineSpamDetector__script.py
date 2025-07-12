```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
extract_data_op = load_component_from_file('components/extract_data.yaml')
preprocess_data_op = load_component_from_file('components/preprocess_data.yaml')
eda_op = load_component_from_file('components/eda.yaml')

# Define the pipeline
@dsl.pipeline(name='sms_spam_classifier', base_image='python:3.8',
              packages_to_install=['requests', 'zipfile', 'pandas', 'matplotlib', 'numpy'])
def sms_spam_classifier():
    # Extract data
    extract_data_task = extract_data_op()
    
    # Preprocess data
    preprocess_data_task = preprocess_data_op(extract_data_task.outputs['output'])
    
    # EDA
    eda_task = eda_op(preprocess_data_task.outputs['output'])

# Compile the pipeline
compiler.Compiler().compile(sms_spam_classifier, 'pipeline.yaml')
```

This script defines a Kubeflow Pipeline named `sms_spam_classifier` that performs spam detection on the SMS Spam Collection dataset. It includes three components: `extract_data`, `preprocess_data`, and `eda`. The pipeline is defined using the `@dsl.pipeline` decorator with the specified name and base image. The components are loaded from YAML files using the `load_component_from_file` function. The pipeline's control flow is sequential, with `extract_data` running first, followed by `preprocess_data`, and finally `eda`. The pipeline is compiled using the `Compiler` class from the `kfp.compiler` module.