```python
from kfp import dsl
import kfp.components as comp

# Define the Print Text component
@comp.component(
    base_image='alpine',
    outputs=[comp.Output('output', type=comp.Text)]
)
def print_text(text: str):
    print(text)

# Define the pipeline
@dsl.pipeline(name="pipeline-with-after")
def after():
    # Task 1: Print '1st task'
    task1 = print_text(text='1st task')

    # Task 2: Print '2nd task' after task1 completes
    task2 = print_text(text='2nd task').after(task1)

    # Task 3: Print '3rd task' after both task1 and task2 complete
    task3 = print_text(text='3rd task').after([task1, task2])
```

This code snippet defines a Kubeflow Pipeline named `pipeline-with-after` that performs three sequential text printing operations. Each operation is implemented as a separate component using the `print_text` function from the `kfp.components` module. The pipeline's control flow is sequential, with each task depending on the completion of the previous one. The pipeline uses Docker containers for component execution and does not use any external libraries.