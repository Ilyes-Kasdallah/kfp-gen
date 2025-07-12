```python
from kfp import dsl
import kfp.components as c

# Define the Print Text component
@c.component(
    base_image="alpine:latest",
    packages_to_install=["bash"],
)
def print_text(text: str):
    """Prints the given text."""
    print(text)

# Define the pipeline
@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Task 1: Print "1st task"
    task_1 = print_text(text="1st task")

    # Task 2: Print "2nd task" after Task 1
    task_2 = print_text(text="2nd task").after(task_1)

    # Task 3: Print "3rd task" after both Task 1 and Task 2
    task_3 = print_text(text="3rd task").after([task_1, task_2])

# Compile the pipeline
compiled_pipeline = kfp.compiler.Compiler().compile(pipeline_with_after, package_path="pipeline-with-after.json")
```

This code snippet defines a Kubeflow Pipeline named `pipeline-with-after` that executes three tasks sequentially. Each task uses a custom containerized component `Print Text`, which prints the provided text to standard output. The `after` construct is used to specify dependencies between tasks, ensuring that Task 2 runs only after Task 1 completes, and Task 3 runs only after both Task 1 and Task 2 complete. The pipeline is then compiled into a JSON artifact named `pipeline-with-after.json`.