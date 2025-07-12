```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='functions-with-outputs')
def lightweight_python_functions_v2_with_outputs(
    first_string=dsl.Inputs.String(default="hello"),
    second_string=dsl.Inputs.String(default=" world"),
    number=dsl.Inputs.Int(default=5),
):
    # Step 1: Concatenate strings
    concat_task = dsl.ContainerOp(
        name='concat-message',
        image='ubuntu',
        command=['bash', '-c'],
        arguments=[
            'echo -n "{}" && echo -n "{}"'.format(first_string, second_string)
        ],
        outputs=[dsl.Outputs.String('result')]
    )

    # Step 2: Add numbers
    add_task = dsl.ContainerOp(
        name='add-numbers',
        image='ubuntu',
        command=['bash', '-c'],
        arguments=[
            'echo $(($first_number + $second_number))'
        ],
        outputs=[dsl.Outputs.Int('sum')]
    )

    # Step 3: Output dataset artifact
    output_dataset_task = dsl.ContainerOp(
        name='output-artifact',
        image='ubuntu',
        command=['bash', '-c'],
        arguments=[
            'echo -n "{}" | tr -d "\n" > /tmp/output.txt'.format(concat_task.outputs['result']),
            'cat /tmp/output.txt | awk "NR=={} {{print}}" >> /tmp/output.txt'.format(number),
            'cat /tmp/output.txt | sed "s/\n/\\n/g" > /tmp/output.txt',
            'cp /tmp/output.txt /tmp/dataset.csv'
        ],
        outputs=[dsl.Outputs.Dataset('dataset')]
    )

    # Step 4: Output named tuple
    output_named_tuple_task = dsl.ContainerOp(
        name='output-named-tuple',
        image='ubuntu',
        command=['bash', '-c'],
        arguments=[
            'cat /tmp/dataset.csv | while read line; do echo -n "$line\n"; done > /tmp/named_tuple_output.txt',
            'awk -F, '{print $1}' /tmp/named_tuple_output.txt > /tmp/scalar_string.txt',
            'awk -F, '{print $2}' /tmp/named_tuple_output.txt > /tmp/metrics.json',
            'awk -F, '{print $3}' /tmp/named_tuple_output.txt > /tmp/model.txt'
        ],
        outputs=[dsl.Outputs.NamedTuple('named_tuple')]
    )
```

This code snippet defines a Kubeflow Pipeline named `functions-with-outputs` with four components: `concat_message`, `add_numbers`, `output_artifact`, and `output_named_tuple`. Each component is defined using the `@dsl.container_op` decorator, which specifies the container image, command, and outputs. The pipeline's control flow is defined using the `@dsl.pipeline` decorator, and the pipeline parameters are specified using the `dsl.inputs` decorator. The pipeline uses the `kfp` library for defining and compiling the pipeline and includes default input values for the pipeline parameters.