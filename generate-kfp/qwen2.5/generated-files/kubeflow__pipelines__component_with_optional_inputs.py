
from kfp import dsl

@dsl.pipeline(name="v2-component-optional-input")
def v2_component_optional_input():
    # Define the component with optional inputs
    @dsl.component(
        name="component_op",
        description="This component takes several optional inputs of various types.",
        parameters={
            "input_string": dsl.Input(type=str),
            "input_boolean": dsl.Input(type=bool),
            "input_dict": dsl.Input(type=dict),
            "input_list": dsl.Input(type=list),
            "input_integer": dsl.Input(type=int)
        },
        outputs={
            "output_string": dsl.Output(type=str),
            "output_boolean": dsl.Output(type=bool),
            "output_dict": dsl.Output(type=dict),
            "output_list": dsl.Output(type=list),
            "output_integer": dsl.Output(type=int)
        }
    )
    def component_op(input_string=None, input_boolean=None, input_dict=None, input_list=None, input_integer=None):
        # Perform some operation on the inputs
        result = f"Result: {input_string} {input_boolean} {input_dict} {input_list} {input_integer}"
        return result

# Example usage
if __name__ == "__main__":
    from kfp import sdk
    sdk.init()

    # Create a pipeline instance
    pipeline = v2_component_optional_input()

    # Execute the pipeline
    pipeline.run()
