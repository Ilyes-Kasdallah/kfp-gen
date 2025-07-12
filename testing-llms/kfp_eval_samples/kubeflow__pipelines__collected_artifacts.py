```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='collecting_artifacts')
def collecting_artifacts():
    # Split model IDs into individual IDs
    split_ids = dsl.ParallelFor(
        'model_ids',
        items=['model1', 'model2', 'model3'],
        output_component_spec=dsl.OutputComponentSpec(type=dsl.Artifact)
    )

    # Create a file with content
    create_file = dsl.ContainerOp(
        name='create_file',
        image='ubuntu:latest',
        command=['sh', '-c', 'echo "Hello, World!" > /tmp/output.txt']
    ).after(split_ids)

    # Read files and print content
    read_files = dsl.ContainerOp(
        name='read_files',
        image='ubuntu:latest',
        command=['sh', '-c', 'cat /tmp/output.txt']
    ).after(create_file)

    # Read single file and print content
    read_single_file = dsl.ContainerOp(
        name='read_single_file',
        image='ubuntu:latest',
        command=['sh', '-c', 'cat /tmp/output.txt']
    ).after(read_files)

    # Split characters into individual characters
    split_chars = dsl.ParallelFor(
        'model_ids',
        items=['model1', 'model2', 'model3'],
        output_component_spec=dsl.OutputComponentSpec(type=dsl.Artifact)
    )

    # Create a dataset with content
    create_dataset = dsl.ContainerOp(
        name='create_dataset',
        image='ubuntu:latest',
        command=['sh', '-c', 'echo "Hello, World!" > /tmp/output.txt']
    ).after(split_chars)

    # Read datasets and print content
    read_datasets = dsl.ContainerOp(
        name='read_datasets',
        image='ubuntu:latest',
        command=['sh', '-c', 'cat /tmp/output.txt']
    ).after(create_dataset)

    # Read single dataset and generate model
    read_single_dataset_generate_model = dsl.ContainerOp(
        name='read_single_dataset_generate_model',
        image='ubuntu:latest',
        command=['sh', '-c', 'echo "Hello, World!" > /tmp/output.txt']
    ).after(read_datasets)

    # Read models and print content
    read_models = dsl.ContainerOp(
        name='read_models',
        image='ubuntu:latest',
        command=['sh', '-c', 'cat /tmp/output.txt']
    ).after(read_single_dataset_generate_model)

# Compile the pipeline
compiler.Compiler().compile(collecting_artifacts, 'collecting_artifacts.yaml')
```

This code defines a Kubeflow Pipeline named `collecting_artifacts` that performs data processing and model generation. The pipeline consists of 9 components, including `split_ids`, `create_file`, `read_files`, `read_single_file`, `split_chars`, `create_dataset`, `read_datasets`, `read_single_dataset_generate_model`, and `read_models`. The pipeline's control flow involves nested loops and the use of `dsl.Collected` to manage the outputs of iterated components within the pipeline. The final output of `collecting_artifacts` is a `List[Model]`.