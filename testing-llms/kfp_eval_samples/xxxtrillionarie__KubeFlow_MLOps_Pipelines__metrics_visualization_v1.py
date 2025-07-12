```python
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='metrics-visualization-v1-pipeline')
def metrics_visualization_pipeline():
    # Define the components
    confusion_visualization = dsl.ContainerOp(
        name='confusion-visualization',
        image='your-image-for-confusion-visualization'
    )

    html_visualization = dsl.ContainerOp(
        name='html-visualization',
        image='your-image-for-html-visualization',
        arguments=[
            '--input', ''
        ]
    )

    markdown_visualization = dsl.ContainerOp(
        name='markdown-visualization',
        image='your-image-for-markdown-visualization'
    )

    roc_visualization = dsl.ContainerOp(
        name='roc-visualization',
        image='your-image-for-roc-visualization'
    )

    table_visualization = dsl.ContainerOp(
        name='table-visualization',
        image='your-image-for-table-visualization'
    )
```

In this solution, we define a Kubeflow Pipeline named `metrics-visualization-v1-pipeline` using the `@dsl.pipeline` decorator. We then define five components: `confusion_visualization`, `html_visualization`, `markdown_visualization`, `roc_visualization`, and `table_visualization`. Each component is represented by a `dsl.ContainerOp` object, specifying the container image and any required arguments. The pipeline structure is straightforward, with each component running independently without any explicit dependencies or control flow mechanisms.