```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
load_data_op = load_component_from_file('load_data.yaml')
prepare_data_op = load_component_from_file('prepare_data.yaml')

# Define the pipeline
@dsl.pipeline(name='diabetes_prediction_pipeline', description='A pipeline for diabetes prediction using XGBoost.')
def diabetes_prediction_pipeline():
    # Load data
    data_output = load_data_op(
        url1="https://raw.githubusercontent.com/daniel88516/diabetes-data/main/10k.csv",
        url2="https://raw.githubusercontent.com/s102401002/kubeflowPipeline/main/data1.csv"
    ).output

    # Prepare data
    prepare_data_op(
        data_input=data_output,
        x_train_output='x_train_output.csv',
        x_test_output='x_test_output.csv',
        y_train_output='y_train_output.csv',
        y_test_output='y_test_output.csv'
    )

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(diabetes_prediction_pipeline)

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment("Diabetes Prediction Experiment")
run = client.run(experiment=experiment, pipeline_spec=pipeline_spec)
```

This code snippet defines a Kubeflow Pipeline named `diabetes_prediction_pipeline` that performs diabetes prediction using XGBoost. It includes two components: `load_data` and `prepare_data`, each defined by their respective YAML files. The pipeline's control flow is sequential, with the `prepare_data` component executing after the `load_data` component completes. The pipeline uses `pandas` for data manipulation and `scikit-learn` for data splitting.