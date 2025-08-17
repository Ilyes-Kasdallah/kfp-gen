import kfp
from kfp import dsl

@dsl.component(
    base_image='python:3.8'
)
def hello_world(text: str) -> str:
    print(text)
    return text

@dsl.pipeline(
    name='hello-world',
    description='A simple pipeline that prints "hi there" to stdout.'
)
def hello_world_pipeline(text: str = 'hi there'):
    hello_task = hello_world(text=text)