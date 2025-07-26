from kfp import pipeline, component

# Import necessary modules
from kfp.dsl import placeholder_if_v2


@pipeline(name="one-step-pipeline-with-if-placeholder-supply-both")
def one_step_pipeline_with_if_placeholder_supply_both(required_input):
    # Define the component
    component_op = placeholder_if_v2(required_input)

    # Define the main task
    main_task = component_op()

    # Return the main task
    return main_task
