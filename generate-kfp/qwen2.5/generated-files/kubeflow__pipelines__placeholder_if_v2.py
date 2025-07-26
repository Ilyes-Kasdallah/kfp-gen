
from kfp import dsl

@dsl.pipeline(name="one-step-pipeline-with-if-placeholder-supply-both")
def one_step_pipeline_with_if_placeholder_supply_both(required_input):
    # Placeholder for placeholder_if_v2
    placeholder_if_v2 = "placeholder_value"
    
    # Component to perform the operation
    component_op = dsl.component(
        name="component_op",
        description="Perform an operation based on the required input.",
        inputs={
            "required_input": dsl.Input(required=True, description="A string (required)")
        },
        outputs={
            "result": dsl.Output(description="The result of the operation")
        },
        operations=[
            {
                "name": "if_placeholder_v2",
                "description": "Check if the required input is 'placeholder_value'. If true, return 'value1'; otherwise, return 'value2'.",
                "inputs": {
                    "input": dsl.Input(required=True, description="The input value to check")
                },
                "outputs": {
                    "output": dsl.Output(description="The result of the operation")
                }
            }
        ]
    )
    
    # Execute the component with the provided input
    result = component_op(required_input)
    
    return result
