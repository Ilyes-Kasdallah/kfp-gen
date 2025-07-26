from kfp import pipeline
from kfp.dsl import component
import pickle


@component
def create_artifact(
    base_image: str = "image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
) -> str:
    """
    Creates a new artifact using the specified base image.

    Args:
    - base_image (str): The base image to use for the artifact.

    Returns:
    - str: The path to the newly created artifact.
    """
    # Placeholder for actual artifact creation logic
    # For demonstration, we'll just return a placeholder string
    return f"artifact_{base_image}"


@pipeline(name="Artifact Pipeline")
def artifact_pipeline():
    """
    A pipeline that creates an artifact using the 'create_artifact' component.
    """
    # Create an artifact using the 'create_artifact' component
    artifact_path = create_artifact()

    # Output the artifact path
    print(f"Artifact Path: {artifact_path}")


# Run the pipeline
artifact_pipeline()
