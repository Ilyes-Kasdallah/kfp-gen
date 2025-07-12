```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
load_data_op = load_component_from_file('load_data.yaml')
prepare_data_op = load_component_from_file('prepare_data.yaml')
train_model_op = load_component_from_file('train_model.yaml')

# Define the pipeline
@dsl.pipeline(name='diabetes_prediction_pipeline')
def diabetes_prediction_pipeline():
    # Step 1: Load data
    data_output = load_data_op()

    # Step 2: Prepare data
    x_train_output, x_test_output, y_train_output, y_test_output = prepare_data_op(data_input=data_output)

    # Step 3: Train model
    train_model_op(x_train=x_train_output, y_train=y_train_output)
```

In this solution, we first load the components using `load_component_from_file` from the `kfp.components` module. We then define the pipeline using the `@dsl.pipeline` decorator with the specified name. Inside the pipeline, we define each step using the corresponding component and connect them sequentially using the `depends_on` attribute. Finally, we return the pipeline definition.