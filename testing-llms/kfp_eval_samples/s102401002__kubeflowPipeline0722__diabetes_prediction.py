```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
load_data_op = load_component_from_file('load_data.yaml')
prepare_data_op = load_component_from_file('prepare_data.yaml')

# Define the pipeline
@dsl.pipeline(name='diabetes_prediction')
def diabetes_prediction():
    # Load data
    data_output = load_data_op(
        url1="https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv",
        url2="https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv"
    )

    # Prepare data
    prepare_data_output = prepare_data_op(
        data_input=data_output.output
    )
```

This code snippet defines a Kubeflow Pipeline named `diabetes_prediction` that includes two components: `load_data` and `prepare_data`. The `load_data` component loads data from two CSV files, cleans it, and prepares it for further use. The `prepare_data` component splits the cleaned data into training, testing, and validation sets. Both components are defined using the `@dsl.component` decorator and run sequentially within the pipeline.