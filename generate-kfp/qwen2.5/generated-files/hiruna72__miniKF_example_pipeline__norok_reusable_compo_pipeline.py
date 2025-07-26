
from kfp import pipeline
from kfp.components import component

@component
def echo(input_1_uri):
    # Read the content of the file
    with open(input_1_uri, 'r') as file:
        content = file.read()
    
    # Print the content
    print(content)

# Define the pipeline
with pipeline("My pipeline") as p:
    # Add the echo component to the pipeline
    p.add_component(echo, name="echo")

# Execute the pipeline
p.run()
