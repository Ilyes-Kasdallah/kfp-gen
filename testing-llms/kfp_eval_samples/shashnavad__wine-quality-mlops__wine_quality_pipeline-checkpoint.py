```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
download_data_op = load_component_from_file('download_data.yaml')
validate_data_op = load_component_from_file('validate_data.yaml')

# Define the pipeline
@dsl.pipeline(name='wine_quality_pipeline')
def wine_quality_pipeline():
    # Download the dataset
    download_data_task = download_data_op()
    
    # Validate the dataset
    validate_data_task = validate_data_op(download_data_task.outputs['dataset_path'])
```

This code defines a Kubeflow Pipeline named `wine_quality_pipeline` with two components: `download_data` and `validate_data`. The `download_data` component downloads the red wine quality dataset from a UCI Machine Learning Repository URL and saves it to a file. The `validate_data` component takes the dataset path as input, performs basic data quality checks, and generates a validation report. The pipeline's control flow is sequential: `validate_data` runs after `download_data`, as it depends on the dataset path generated by the first component.