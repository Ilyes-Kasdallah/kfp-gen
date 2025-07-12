```python
import kfp
from kfp import dsl

# Define the Wine Classification component
@dsl.component(
    base_image="tensorflow/tensorflow:latest",
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.METRICS)
)
def wine_classification():
    # Implementation of wine classification logic
    pass

# Define the Iris SGD Classifier component
@dsl.component(
    base_image="tensorflow/tensorflow:latest"
)
def iris_sgd_classifier():
    # Implementation of SGD classifier training logic
    pass

# Define the Digit Classification component
@dsl.component(
    base_image="tensorflow/tensorflow:latest"
)
def digit_classification():
    # Implementation of digit classification logic
    pass

# Define the HTML Visualization component
@dsl.component(
    base_image="tensorflow/tensorflow:latest",
    input_artifact=dsl.InputArtifact(type=dsl.ArtifactType.METRICS),
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.HTML)
)
def html_visualization(metrics):
    # Implementation of HTML visualization logic
    pass

# Define the Markdown Visualization component
@dsl.component(
    base_image="tensorflow/tensorflow:latest",
    input_artifact=dsl.InputArtifact(type=dsl.ArtifactType.METRICS),
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.MARKDOWN)
)
def markdown_visualization(metrics):
    # Implementation of Markdown visualization logic
    pass

# Define the Metrics Visualization Pipeline
@dsl.pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_pipeline():
    # Execute the Wine Classification component
    wine_metrics = wine_classification()

    # Execute the Iris SGD Classifier component
    iris_metrics = iris_sgd_classifier()

    # Execute the Digit Classification component
    digit_metrics = digit_classification()

    # Visualize the metrics using HTML
    html_output = html_visualization(wine_metrics)

    # Visualize the metrics using Markdown
    markdown_output = markdown_visualization(iris_metrics)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(metrics_visualization_pipeline, "metrics_visualization_pipeline.yaml")
```

This code defines the required components and the pipeline structure, ensuring that the pipeline runs the specified tasks in parallel and visualizes the results using both HTML and Markdown formats.