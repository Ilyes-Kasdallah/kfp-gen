from asyncio.windows_events import NULL
import kfp.dsl as dsl
import kfp.compiler as compiler
import kfp.components as comp


def add(a: float, b: float) -> float:
  '''Calculates sum of two arguments'''
  return a + b

add_op = comp.create_component_from_func(
    add, output_component_file='add_component.yaml')

def echo_out(result: float) -> NULL:
    print("The result is :", result)

echo_op = comp.create_component_from_func(echo_out)


@dsl.pipeline(
    name='add_pipeline',
    description='sample pipeline to add two numbers and then print the result.'
)

def add_pipeline(
  a='1',
  b='7',
):
  # Passes a pipeline parameter and a constant value to the `add_op` factory
  # function.
  first_add_task = add_op(a, 4)
  # Passes an output reference from `first_add_task` and a pipeline parameter
  # to the `add_op` factory function. For operations with a single return
  # value, the output reference can be accessed as `task.output` or
  # `task.outputs['output_name']`.
  second_add_task = add_op(first_add_task.output, b)

  # Print the results
  third_echo_task = echo_op(second_add_task.output)

if __name__ == '__main__':
    compiler.Compiler().compile(add_pipeline, __file__ + '.yaml')