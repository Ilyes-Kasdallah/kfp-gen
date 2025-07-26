
from kfp import dsl

@dsl.pipeline(name="loop_consume_upstream")
def loop_consume_upstream():
    # Define the split_input component
    split_input = dsl.component(
        name="split_input",
        description="Splits a comma-separated string into a list of strings.",
        inputs={
            "input": dsl.Input("input", type=dsl.StringType())
        },
        outputs={
            "output": dsl.Output("output", type=dsl.ListType())
        },
        code="""
        def split_input(input_str):
            return input_str.split(',')
        """
    )

    # Define the parallel_consume_upstream component
    parallel_consume_upstream = dsl.component(
        name="parallel_consume_upstream",
        description="Consumes files in parallel.",
        inputs={
            "input": dsl.Input("input", type=dsl.StringType())
        },
        outputs={
            "output": dsl.Output("output", type=dsl.StringType())
        },
        code="""
        from kfp import pipeline
        from kfp.components import pipeline_function

        @pipeline_function
        def parallel_consume_upstream(input_str):
            # Split the input string into a list of strings
            output_list = split_input(input_str)
            # Return the list of output strings
            return output_list
        """
    )

    # Use the parallel_consume_upstream component in the pipeline
    result = parallel_consume_upstream(input="component1,component2,component3")

    # Print the result
    print(result)
