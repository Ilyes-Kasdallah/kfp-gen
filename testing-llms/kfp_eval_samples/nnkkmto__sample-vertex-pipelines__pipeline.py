```python
import kfp
from kfp import dsl

# Load component definitions from the component directory
kfp.components.load_component_from_file('component/split_sentence/component.yaml')
kfp.components.load_component_from_file('component/print_word/component.yaml')

# Define the pipeline
@dsl.pipeline(name='sample-pipeline', description='A sample pipeline for text processing.')
def sample_pipeline(sentence: str):
    # Split the sentence into words
    split_words = dsl.ParallelFor(
        dsl.ContainerOp(
            name='split_sentence',
            image='gcr.io/your-project/service-account-image',
            arguments=['--input', sentence],
            outputs=[dsl.OutputPath('words')]
        )
    )

    # Print each word
    for word in split_words:
        print_word = dsl.ContainerOp(
            name='print_word',
            image='gcr.io/your-project/service-account-image',
            arguments=['--input', word.outputs['words']],
            outputs=[]
        )

# Compile the pipeline
compiler.Compiler().compile(sample_pipeline, 'pipeline.json')

# Deploy the pipeline
client = kfp.Client()
client.create_run_from_pipeline_package('pipeline.json', arguments={'sentence': 'Hello Vertex Pipelines'})
```

In this solution, we define a Kubeflow Pipeline named `sample-pipeline` that processes a given sentence by splitting it into words and printing each word. We use the `@dsl.pipeline` decorator to specify the pipeline's name and description. The `sample_pipeline` function contains a `ParallelFor` loop that executes the `split_sentence` component concurrently. Each word processed by `split_sentence` is then passed to the `print_word` component. The pipeline is compiled into a `pipeline.json` file and deployed to Google Cloud AI Platform Pipelines using the `kfp.Client` class.