```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_url

# Load the components
get_raw_data = load_component_from_url('https://raw.githubusercontent.com/pavan-kumar-99/ml-ops/master/components/getRawData.yaml')
split_train_test = load_component_from_url('https://raw.githubusercontent.com/pavan-kumar-99/ml-ops/master/components/SplitTrainTest.yaml')

# Define the pipeline
@dsl.pipeline(name='DataSplitPipeline')
def DataSplitPipeline():
    # Get raw data
    get_raw_data_op = get_raw_data()
    
    # Split train test
    split_train_test_op = split_train_test(get_raw_data_op.output)

# Compile the pipeline
compiler.Compiler().compile(DataSplitPipeline, 'TestTrainSplit.json')
```

This code defines a Kubeflow Pipeline named `DataSplitPipeline` that performs a train-test split on a dataset. It includes two components: `getRawData` and `SplitTrainTest`. The pipeline's control flow is sequential, with `SplitTrainTest` executing after `getRawData`. The pipeline utilizes the `kfp` and `sklearn` libraries.