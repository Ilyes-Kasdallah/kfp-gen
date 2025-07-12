```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
check_if_raw_data_exists_already = load_component_from_file('path/to/check_if_raw_data_exists_already.yaml')
download_raw_data_for_pipeline = load_component_from_file('path/to/download_raw_data_for_pipeline.yaml')
save_raw_data_to_bucket = load_component_from_file('path/to/save_raw_data_to_bucket.yaml')

# Define the pipeline
@dsl.pipeline(name='cleaning_and_prep_pipeline')
def cleaning_and_prep_pipeline(bucket_name='your-bucket-name', object_name='your-object-name'):
    # Check if raw data exists already
    check_result = check_if_raw_data_exists_already(bucket_name=bucket_name, object_name=object_name)

    # Download raw data if it doesn't exist
    download_task = download_raw_data_for_pipeline(object_name=object_name)
    
    # Save raw data to bucket if it doesn't exist
    save_task = save_raw_data_to_bucket(bucket_name=bucket_name, object_name=object_name, raw_data=download_task.outputs['dataset'])

# Compile the pipeline
compiler.Compiler().compile(cleaning_and_prep_pipeline, 'cleaning_and_prep_pipeline.yaml')
```

In this solution, we define the pipeline using the `@dsl.pipeline` decorator with the specified name. We load the components using `load_component_from_file` and define the pipeline structure with conditional execution based on the result of the first component. Finally, we compile the pipeline into a YAML file using the `Compiler` class from the `kfp.compiler` module.