from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='v2-container-component-no-input')
def pipeline_container_no_input():
    # Define the component
    @dsl.component(
        base_image='python:3.7',
        command=['echo', 'hello world']
    )
    def container_no_input():
        pass

    # Execute the component
    container_no_input()
