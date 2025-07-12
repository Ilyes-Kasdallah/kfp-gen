```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
load_data_op = load_component_from_file('load_data.yaml')
prepare_data_op = load_component_from_file('prepare_data.yaml')
train_model_op = load_component_from_file('train_model.yaml')

# Define the pipeline
@dsl.pipeline(name='HypertensionPredictionPipeline')
def hypertension_prediction():
    # Step 1: Load Data
    data_output = load_data_op()

    # Step 2: Prepare Data
    X_train_output, X_test_output, X_val_output, Y_train_output, Y_test_output, Y_val_output = prepare_data_op(data_input=data_output)

    # Step 3: Train Model
    model_output = train_model_op(X_train=X_train_output, Y_train=Y_train_output, X_val=X_val_output, Y_val=Y_val_output)
```

In this solution, we define a Kubeflow Pipeline named `HypertensionPredictionPipeline` using the `@dsl.pipeline` decorator. We load the required components using `load_component_from_file` and define the pipeline steps sequentially. Each step depends on the previous one, ensuring the pipeline executes in the correct order. The pipeline uses pandas and scikit-learn libraries for data manipulation and model training, respectively.