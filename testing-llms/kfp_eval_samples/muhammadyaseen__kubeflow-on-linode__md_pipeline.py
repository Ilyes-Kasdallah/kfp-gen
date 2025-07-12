```python
import kfp
from kfp import dsl

# Import necessary libraries
import pandas as pd

# Define the write_simple_markdown_table component
@dsl.component(
    packages_to_install=['pandas'],
    output_artifacts=[
        dsl.OutputArtifact(type=dsl.ArtifactType.MARKDOWN)
    ]
)
def write_simple_markdown_table():
    # Create a simple table
    data = {
        'Animal': ['Dog', 'Cat', 'Bird']
    }
    df = pd.DataFrame(data)
    
    # Convert DataFrame to Markdown
    markdown_table = df.to_markdown(index=False)
    
    return markdown_table

# Define the write_simple_markdown_heading component
@dsl.component(
    output_artifacts=[
        dsl.OutputArtifact(type=dsl.ArtifactType.MARKDOWN)
    ]
)
def write_simple_markdown_heading():
    # Generate a Markdown heading
    markdown_content = "# Hello world\nThis is some additional content."
    
    return markdown_content

# Define the vertex_ai_markdown_example component
@dsl.component(
    output_artifacts=[
        dsl.OutputArtifact(type=dsl.ArtifactType.MARKDOWN)
    ]
)
def vertex_ai_markdown_example():
    # Create a more complex table visualization example
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]
    }
    df = pd.DataFrame(data)
    
    # Convert DataFrame to Markdown
    markdown_table = df.to_markdown(index=False)
    
    return markdown_table

# Define the write_pandas_dataframe_as_markdown component
@dsl.component(
    output_artifacts=[
        dsl.OutputArtifact(type=dsl.ArtifactType.MARKDOWN)
    ]
)
def write_pandas_dataframe_as_markdown():
    # Create a DataFrame and convert it to Markdown
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]
    }
    df = pd.DataFrame(data)
    
    # Convert DataFrame to Markdown
    markdown_df = df.to_markdown(index=False)
    
    return markdown_df

# Define the md_pipeline function
@dsl.pipeline(name='md-pipeline')
def md_pipeline():
    # Execute the components sequentially
    write_simple_markdown_table_op = write_simple_markdown_table()
    write_simple_markdown_heading_op = write_simple_markdown_heading()
    vertex_ai_markdown_example_op = vertex_ai_markdown_example()
    write_pandas_dataframe_as_markdown_op = write_pandas_dataframe_as_markdown()

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(md_pipeline)

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment('My Experiment')
run = client.run(pipeline_spec=pipeline_spec, experiment=experiment.name)
```

This code defines a Kubeflow Pipeline named `md-pipeline` that performs Markdown visualization by executing four components: `write_simple_markdown_table`, `write_simple_markdown_heading`, `vertex_ai_markdown_example`, and `write_pandas_dataframe_as_markdown`. Each component outputs a Markdown artifact, which is then used in subsequent components to generate more complex Markdown content. The pipeline is compiled and submitted to a Kubeflow cluster for execution.