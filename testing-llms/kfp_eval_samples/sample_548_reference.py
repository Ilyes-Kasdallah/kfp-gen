import kfp.dsl as dsl

import my_components as comps

# Define a pipeline
@dsl.pipeline(
    name='Addition pipeline',
    description='A toy pipeline that performs addition calculations.'
)
def add_pipeline(
    a: float = 1,
    b: float = 7,
):
    first_add_task = comps.add(a, 4)
    second_add_task = comps.add(first_add_task.output, b)