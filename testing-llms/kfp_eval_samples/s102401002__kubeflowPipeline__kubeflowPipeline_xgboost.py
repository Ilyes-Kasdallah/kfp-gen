```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
load_data_op = load_component_from_file('load_data.yaml')
prepare_data_op = load_component_from_file('prepare_data.yaml')

# Define the pipeline
@dsl.pipeline(name='diabetes_prediction_pipeline')
def diabetes_prediction_pipeline():
    # Step 1: Load data
    load_data_task = load_data_op(
        url1="https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv",
        url2="https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv"
    )

    # Step 2: Prepare data
    prepare_data_task = prepare_data_op(
        input_artifact=load_data_task.outputs['output']
    )
```

This code snippet defines a Kubeflow Pipeline named `diabetes_prediction_pipeline` that performs diabetes prediction. It includes two components: `load_data` and `prepare_data`. The `load_data` component downloads data from specified URLs, cleans it, and saves it as an Artifact. The `prepare_data` component takes this Artifact as input, splits the data into training and testing sets, and saves the results as separate Artifacts. The pipeline's control flow is sequential, with `prepare_data` running after `load_data`.