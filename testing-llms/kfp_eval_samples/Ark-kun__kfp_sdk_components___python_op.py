```python
from kfp import dsl

# Define custom input/output types
class InputPath(dsl.Input):
    pass

class InputTextFile(dsl.Input):
    pass

class InputBinaryFile(dsl.Input):
    pass

class OutputPath(dsl.Output):
    pass

class OutputTextFile(dsl.Output):
    pass

class OutputBinaryFile(dsl.Output):
    pass

# Define a component that reads a text file and returns its contents
@dsl.component(
    output_artifact=dsl.Artifact(type=dsl.ArtefactType.TEXT),
    input_artifacts=[InputTextFile(path='input.txt')]
)
def read_text_file(input_path: InputTextFile) -> str:
    with open(input_path.path, 'r') as f:
        return f.read()

# Define a component that writes a string to a text file
@dsl.component(
    input_artifact=dsl.Artifact(type=dsl.ArtefactType.TEXT),
    output_artifact=dsl.Artifact(type=dsl.ArtefactType.TEXT),
    input_artifacts=[InputTextFile(path='output.txt'), OutputTextFile(path='output.txt')]
)
def write_text_file(input_text: InputTextFile, output_text: OutputTextFile) -> None:
    with open(output_text.path, 'w') as f:
        f.write(input_text.text)

# Define the main pipeline
@dsl.pipeline(name="pipeline_from_func")
def pipeline_from_func():
    # Read the input text file
    input_text = read_text_file(input_path=InputTextFile(path='input.txt'))
    
    # Write the processed text to an output text file
    write_text_file(input_text=input_text, output_text=OutputTextFile(path='output.txt'))

# Execute the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(pipeline_from_func, "pipeline_from_func.yaml")
```

This code snippet defines two components: `read_text_file` and `write_text_file`. The `read_text_file` component takes an input text file and returns its contents as a string. The `write_text_file` component takes an input text file and an output text file, writes the input text to the output text file, and does not return any value. The `pipeline_from_func` is the main pipeline that orchestrates these components by reading the input text file, processing it, and writing the result to an output text file.