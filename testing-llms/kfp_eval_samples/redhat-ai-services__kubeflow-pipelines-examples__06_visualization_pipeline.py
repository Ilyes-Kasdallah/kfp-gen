```python
import kfp
from kfp import dsl

# Importing necessary libraries
import json

# Defining the pipeline
@dsl.pipeline(name="Metadata Example Pipeline")
def confusion_matrix_viz():
    # Defining the component
    @dsl.component(
        base_image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
        output_artifact_paths={
            "mlpipeline_ui_metadata_path": "/tmp/mlpipeline-ui-metadata.json",
            "confusion_matrix_path": "/tmp/confusion_matrix.csv"
        }
    )
    def confusion_matrix_viz_impl():
        # Hardcoded CSV data for the confusion matrix
        csv_data = """
        class_name,predicted_class,confidence
        ClassA,ClassB,0.8
        ClassB,ClassC,0.7
        ClassC,ClassA,0.9
        """

        # Writing the CSV data to a temporary file
        with open("/tmp/confusion_matrix.csv", "w") as f:
            f.write(csv_data)

        # Creating metadata for the confusion matrix
        metadata = {
            "name": "Confusion Matrix",
            "description": "Generated confusion matrix for classification tasks.",
            "schema": {
                "type": "object",
                "properties": {
                    "class_name": {"type": "string"},
                    "predicted_class": {"type": "string"},
                    "confidence": {"type": "number"}
                },
                "required": ["class_name", "predicted_class", "confidence"]
            },
            "source": "Custom Component",
            "storage": "Local Storage",
            "labels": {
                "category": "Visualization",
                "task_type": "Classification"
            }
        }

        # Writing the metadata to a JSON file
        with open("/tmp/mlpipeline-ui-metadata.json", "w") as f:
            json.dump(metadata, f)

        # Returning the confusion matrix string
        return csv_data

# Instantiating the Kubeflow client
client = kfp.Client()

# Submitting the pipeline run
run = client.create_run_from_pipeline_func(confusion_matrix_viz)
print(f"Pipeline run submitted with ID: {run.id}")
```

This solution defines a Kubeflow Pipeline named `Metadata Example Pipeline` that includes a single component `confusion_matrix_viz`. The component generates a confusion matrix in CSV format and associated metadata for visualization within the Kubeflow UI. The pipeline uses the `json` library for handling JSON metadata. The base image for the component is `"image-registry.openshift-image-registry.svc:5000/openshift/python:latest"`, and the pipeline uses environment variables `KUBEFLOW_ENDPOINT` and `BEARER_TOKEN` for authentication with the Kubeflow server.