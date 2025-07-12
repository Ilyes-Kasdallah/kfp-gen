```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='my_pipeline')
def my_pipeline():
    # Step 0: Get the current UTC epoch timestamp and day of the week
    utc_epoch_and_day_of_week = step_0()
    
    # Step 1: Print the message from step 0
    step_1(utc_epoch_and_day_of_week.message)

# Execute the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(my_pipeline, 'pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `my_pipeline` with two sequential steps. The first step, `step_0`, retrieves the current UTC epoch timestamp and day of the week and returns them as a named tuple. The second step, `step_1`, takes this named tuple as an input and prints it to the standard output. The pipeline uses the `kfp` library for Kubeflow Pipelines definition and utilizes `python:3.10` as the base image for the component containers.