```python
import kfp
from kfp import dsl

# Define the first component
@dsl.component(
    base_image='library/bash:4.4.23',
    outputs=['output']
)
def echo1(text1='message 1'):
    print(text1)

# Define the second component
@dsl.component(
    base_image='library/bash:4.4.23',
    outputs=['output']
)
def echo2(text2='message 2'):
    print(text2)

# Define the pipeline
@dsl.pipeline(name='Execution order pipeline')
def execution_order():
    step1_task = echo1()
    step2_task = echo2().after(step1_task)

# Compile the pipeline
compiler.Compiler().compile(execution_order, 'execution_order.yaml')
```

This code snippet defines a Kubeflow Pipeline named `Execution order pipeline` with two components: `echo1` and `echo2`. The `echo1` component prints the string 'message 1' to the standard output, while the `echo2` component prints 'message 2'. The control flow is sequential, with `echo2` running after `echo1` is complete. The pipeline is compiled into a YAML file named `execution_order.yaml` for deployment on Kubeflow.