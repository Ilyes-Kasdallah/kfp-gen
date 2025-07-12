```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load the components
preprocess_data_op = load_component_from_file('preprocess_data.yaml')
map_label_op = load_component_from_file('map_label.yaml')

# Define the pipeline
@dsl.pipeline(name='data_ingestion_pipeline')
def data_ingestion_pipeline(df_path: str, to_keep: list, data: str, df_output_path: str, mapped_df_path: str):
    # Preprocess the data
    preprocess_data_task = preprocess_data_op(
        df_path=df_path,
        to_keep=to_keep,
        data=data,
        df_output_path=df_output_path
    )
    
    # Map labels
    map_label_task = map_label_op(
        df_path=preprocess_data_task.outputs['df']
    )

# Compile the pipeline
kfp.compiler.Compiler().compile(data_ingestion_pipeline, 'data_ingest_fns.py')
```

In this solution, we define the `data_ingestion_pipeline` function using the `@dsl.pipeline` decorator. We load the `preprocess_data` and `map_label` components using `load_component_from_file`. Inside the pipeline, we create tasks for each component and connect them sequentially using the `outputs` attribute of one task as the input for another. Finally, we compile the pipeline using the `Compiler()` class and save it to a file named `data_ingest_fns.py`.