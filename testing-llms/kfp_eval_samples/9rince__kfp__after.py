```python
from kfp import dsl
import kfp.components as comp

# Define the custom containerized component for task1
@comp.component(
    base_image="ubuntu",
    packages_to_install=["python"],
    outputs=[comp.OutputArtifact("output")]
)
def task1():
    print("1st task")

# Define the custom containerized component for task2
@comp.component(
    base_image="ubuntu",
    packages_to_install=["python"],
    inputs=[comp.InputArtifact("input")],
    outputs=[comp.OutputArtifact("output")]
)
def task2(input_artifact):
    print("2nd task")
    input_artifact.write_text("Task2 completed")

# Define the custom containerized component for task3
@comp.component(
    base_image="ubuntu",
    packages_to_install=["python"],
    inputs=[comp.InputArtifact("input1"), comp.InputArtifact("input2")],
    outputs=[comp.OutputArtifact("output")]
)
def task3(input1_artifact, input2_artifact):
    print("3rd task")
    input1_artifact.write_text("Task3 completed")
    input2_artifact.write_text("Task3 completed")

# Define the Kubeflow Pipeline named 'pipeline-with-after'
@dsl.pipeline(name='pipeline-with-after')
def pipeline_with_after():
    # Create an artifact for task1's output
    task1_output = task1().outputs['output']
    
    # Create an artifact for task2's input
    task2_input = task1_output
    
    # Run task2 after task1
    task2(task2_input)
    
    # Create an artifact for task3's input
    task3_input1 = task1_output
    task3_input2 = task2_output
    
    # Run task3 after both task1 and task2
    task3(task3_input1, task3_input2)

# Compile the pipeline
kfp.compiler.Compiler().compile(pipeline_with_after, 'after.yaml')
```

This code snippet defines a Kubeflow Pipeline named `pipeline-with-after` that performs three sequential text printing operations. Each operation is performed by a custom containerized component, and the pipeline uses the `after` construct to define the execution order. The pipeline utilizes the `kfp` library and custom containerized components defined using a YAML specification.