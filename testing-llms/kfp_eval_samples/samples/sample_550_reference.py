import kfp.dsl as dsl
import my_components as comps

@dsl.pipeline(
   name='calculation-pipeline',
   description='An example pipeline that performs arithmetic calculations.',
)
def calc_pipeline(
   a: float=1,
   b: float=7,
   c: float=17,
):
    # Passes a pipeline parameter and a constant value as operation arguments.
    add_task = comps.add(a, 4) # The add_op factory function returns
                            # a dsl.ContainerOp class instance. 

    # Passes the output of the add_task and a pipeline parameter as operation
    # arguments. For an operation with a single return value, the output
    # reference is accessed using `task.output` or
    # `task.outputs['output_name']`.
    divmod_task = comps.my_divmod(add_task.output, b)

    # For an operation with multiple return values, output references are
    # accessed as `task.outputs['output_name']`.
    result_task = comps.add(divmod_task.outputs['quotient'], c)
