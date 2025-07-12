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
    # Implementation of Iris SGD classifier logic
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
    input_artifacts=[dsl.InputArtifact(type=dsl.ArtifactType.METRICS)]
)
def html_visualization(metrics):
    # Implementation of HTML visualization logic
    pass

# Define the Markdown Visualization component
@dsl.component(
    base_image="tensorflow/tensorflow:latest",
    input_artifacts=[dsl.InputArtifact(type=dsl.ArtifactType.METRICS)]
)
def markdown_visualization(metrics):
    # Implementation of Markdown visualization logic
    pass

# Define the Metrics Visualization Pipeline
@dsl.pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_pipeline():
    # Run wine classification
    wine_metrics = wine_classification()
    
    # Run Iris SGD Classifier
    iris_metrics = iris_sgd_classifier()
    
    # Run digit classification
    digit_metrics = digit_classification()
    
    # Visualize metrics using HTML
    html_output = html_visualization(wine_metrics)
    
    # Visualize metrics using Markdown
    markdown_output = markdown_visualization(iris_metrics)

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(metrics_visualization_pipeline, package_path='metrics_visualization_v2_test.yaml')

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment("Metrics Visualization Experiment")
run = client.run(experiment.id, pipeline_spec=pipeline_spec)
```

This code defines the required components and the pipeline structure, including the dependencies between them. It also includes placeholders for the actual implementation of each component's logic. The pipeline is then compiled into a YAML file and submitted to a Kubeflow cluster for execution.