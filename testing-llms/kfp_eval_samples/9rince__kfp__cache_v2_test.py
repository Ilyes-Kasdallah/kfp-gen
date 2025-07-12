```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load the preprocess component
preprocess_op = load_component_from_file('path/to/preprocess.component.yaml')

# Load the train-op component
train_op = load_component_from_file('path/to/train-op.component.yaml')

# Define the pipeline
@dsl.pipeline(name='two_step_pipeline')
def two_step_pipeline(some_int):
    # Execute the preprocess component
    preprocess_task = preprocess_op(
        some_int=some_int,
        uri='input_uri'
    )
    
    # Execute the train-op component
    train_task = train_op(
        output_dataset_one=preprocess_task.outputs['output_dataset_one'],
        num_steps=some_int
    )

# Compile the pipeline
kfp.compiler.Compiler().compile(two_step_pipeline, 'two_step_pipeline.tar.gz')
```

In this solution, we first load the `preprocess` and `train-op` components using `load_component_from_file`. We then define the `two_step_pipeline` function using the `@dsl.pipeline` decorator. Inside the pipeline, we execute the `preprocess` component and store its output in a task variable. Next, we execute the `train-op` component, passing the `output_dataset_one` artifact from the `preprocess` component and the `num_steps` parameter. Finally, we compile the pipeline into a tarball using `kfp.compiler.Compiler()`.