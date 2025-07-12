```python
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='hello-world')
def hello_world(text='hi there'):
    # Define the component
    @dsl.component(
        base_image='python:3.8-slim',
        packages_to_install=['numpy'],
        outputs=[dsl.Output('output')]
    )
    def hello_world(text):
        print(text)
        return text

    # Execute the component
    hello_world(text=text)

# Compile the pipeline
pipeline = dsl.Pipeline.from_function(hello_world)
pipeline.save('hello_world_pipeline.json')
```