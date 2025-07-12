```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the preprocess component
preprocess_op = load_component_from_file('path/to/preprocess.component.yaml')

# Load the train-op component
train_op = load_component_from_file('path/to/train-op.component.yaml')

# Define the two-step pipeline
@dsl.pipeline(name='two_step_pipeline')
def two_step_pipeline(some_int=42, uri='https://example.com/data'):
    # Execute the preprocess step
    preprocess_result = preprocess_op(
        some_int=some_int,
        uri=uri
    )

    # Execute the train step
    model = train_op(
        dataset=preprocess_result.outputs['dataset'],
        num_steps=some_int
    )
```

In this solution, we first load the `preprocess` and `train-op` components using `load_component_from_file`. We then define the `two_step_pipeline` using the `@dsl.pipeline` decorator. Inside the pipeline, we execute the `preprocess` step by passing the `some_int` and `uri` parameters. The result of the `preprocess` step is stored in the `preprocess_result` variable. Next, we execute the `train-op` step by passing the `dataset` output from the `preprocess` step and the `some_int` parameter. The resulting `model` is stored in the `model` variable.