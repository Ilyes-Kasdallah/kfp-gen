```python
from kfp import dsl

# Define the create_pvc component
@dsl.component(
    base_image="gcr.io/kubernetes-samples/pvc-demo",
    output_artifact=dsl.OutputArtifact(type=dsl.VOLUME),
    metadata={
        "description": "Creates a PersistentVolumeClaim"
    }
)
def create_pvc():
    pass

# Define the preprocess component
@dsl.component(
    base_image="gcr.io/compose-flask/hub:v6",
    input_artifacts=[dsl.InputArtifact(type=dsl.DATASET)],
    output_artifact=dsl.OutputArtifact(type=dsl.FILE),
    metadata={
        "description": "Preprocesses the dataset"
    }
)
def preprocess(project):
    pass

# Define the build component
@dsl.component(
    base_image="gcr.io/compose-flask/build:v6",
    input_artifacts=[
        dsl.InputArtifact(type=dsl.DATASET),
        dsl.InputArtifact(type=dsl.FILE),
        dsl.InputArtifact(type=dsl.FILE)
    ],
    output_artifact=dsl.OutputArtifact(type=dsl.FILE),
    metadata={
        "description": "Builds the model"
    }
)
def build(project, preprocessed, preprocessed2):
    pass

# Define the pipeline
@dsl.pipeline(name="Kubeflow Pipeline Test")
def pipeline(project):
    # Create PVC
    pvc = create_pvc()
    
    # Preprocess dataset
    preprocess_task = preprocess(project=project, artifacts=pvc.outputs['volume'])
    
    # Build model
    build_task = build(project=project, artifacts=preprocess_task.outputs['file'], artifacts=preprocess_task.outputs['file2'])

# Compile the pipeline
if __name__ == "__main__":
    from kfp.compiler import.Compiler
    compiler = Compiler()
    pipeline_spec = compiler.compile(pipeline, package_path='pipeline.yaml')
```

This code defines the required components and the pipeline structure, ensuring it follows the Kubeflow Pipelines SDK guidelines. The pipeline includes dependencies between components and uses the specified images and volumes.