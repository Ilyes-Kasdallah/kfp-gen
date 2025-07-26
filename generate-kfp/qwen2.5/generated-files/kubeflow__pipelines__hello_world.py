
from kfp import dsl

@dsl.pipeline(name='hello-world')
def hello_world(text='hi there'):
    # Define the component
    hello_world = dsl.component(
        name='hello_world',
        implementation=lambda text: print(text)
    )
    
    # Use the component in the pipeline
    return hello_world(text)
