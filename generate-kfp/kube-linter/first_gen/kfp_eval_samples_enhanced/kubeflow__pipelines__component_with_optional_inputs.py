import kfp
from kfp.dsl import component, pipeline


@dsl.pipeline(name="v2-component-optional-input")
def v2_component_optional_input():
    # Define the component with optional inputs
    @component(
        name="component_op",
        description="This is a component that takes several optional inputs.",
        parameters={
            "input_string": kfp.dsl.Input(type=kfp.dsl.String),
            "input_boolean": kfp.dsl.Input(type=kfp.dsl.Boolean),
            "input_dict": kfp.dsl.Input(type=kfp.dsl.Dict),
            "input_list": kfp.dsl.Input(type=kfp.dsl.List),
            "input_integer": kfp.dsl.Input(type=kfp.dsl.Integer),
        },
        outputs={
            "output_string": kfp.dsl.Output(type=kfp.dsl.String),
            "output_boolean": kfp.dsl.Output(type=kfp.dsl.Boolean),
            "output_dict": kfp.dsl.Output(type=kfp.dsl.Dict),
            "output_list": kfp.dsl.Output(type=kfp.dsl.List),
            "output_integer": kfp.dsl.Output(type=kfp.dsl.Integer),
        },
    )
    def component_op(
        input_string=None,
        input_boolean=None,
        input_dict=None,
        input_list=None,
        input_integer=None,
    ):
        # Implement the logic for the component
        output_string = f"Output String: {input_string}"
        output_boolean = f"Output Boolean: {input_boolean}"
        output_dict = f"Output Dictionary: {input_dict}"
        output_list = f"Output List: {input_list}"
        output_integer = f"Output Integer: {input_integer}"
        return {
            "output_string": output_string,
            "output_boolean": output_boolean,
            "output_dict": output_dict,
            "output_list": output_list,
            "output_integer": output_integer,
        }


# Run the pipeline
if __name__ == "__main__":
    v2_component_optional_input()
