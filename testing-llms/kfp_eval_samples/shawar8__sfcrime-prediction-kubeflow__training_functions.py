```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_text

# Load the components
get_train_test_split_op = load_component_from_text("""
apiVersion: kfp.v2.components/v1
kind: Component
metadata:
  name: get_train_test_split
spec:
  implementation:
    container:
      image: python:3.9
      command:
        - python
        - main.py
        - --df-path
        - ${{inputs.parameters.df_path}}
        - --label-column
        - ${{inputs.parameters.label_column}}
        - --test-size
        - ${{inputs.parameters.test_size}}
        - --n-tries
        - ${{inputs.parameters.n_tries}}
      args:
        - --output-x-train
        - ${{outputs.artifacts.output_x_train.path}}
        - --output-x-test
        - ${{outputs.artifacts.output_x_test.path}}
        - --output-y-train
        - ${{outputs.artifacts.output_y_train.path}}
        - --output-y-test
        - ${{outputs.artifacts.output_y_test.path}}
        - --divergence-output-dict
        - ${{outputs.artifacts.divergence_output_dict.path}}
""")
prepare_data_for_training_op = load_component_from_text("""
apiVersion: kfp.v2.components/v1
kind: Component
metadata:
  name: prepare_data_for_training
spec:
  implementation:
    container:
      image: python:3.9
      command:
        - python
        - main.py
        - --input-x-train
        - ${{inputs.artifacts.input_x_train.path}}
        - --input-x-test
        - ${{inputs.artifacts.input_x_test.path}}
        - --input-y-train
        - ${{inputs.artifacts.input_y_train.path}}
        - --input-y-test
        - ${{inputs.artifacts.input_y_test.path}}
      args:
        - --output-prepared-data
        - ${{outputs.artifacts.output_prepared_data.path}}
""")

# Define the pipeline
@dsl.pipeline(name="training_pipeline")
def training_pipeline(df_path: str, label_column: str, test_size: float, n_tries: int):
    # Get train/test split
    get_train_test_split_task = get_train_test_split_op(
        df_path=df_path,
        label_column=label_column,
        test_size=test_size,
        n_tries=n_tries
    )

    # Prepare data for training
    prepare_data_for_training_task = prepare_data_for_training_op(
        input_x_train=get_train_test_split_task.outputs['output_x_train'],
        input_x_test=get_train_test_split_task.outputs['output_x_test'],
        input_y_train=get_train_test_split_task.outputs['output_y_train'],
        input_y_test=get_train_test_split_task.outputs['output_y_test']
    )
```

This solution defines a Kubeflow Pipeline named `training_pipeline` with two components: `get_train_test_split` and `prepare_data_for_training`. The `get_train_test_split` component splits the dataset into training and testing sets, while the `prepare_data_for_training` component prepares the data for further processing. The pipeline is executed sequentially, with the output of one task being used as an input for the next.