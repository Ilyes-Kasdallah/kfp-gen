import kfp
from kfp.dsl import pipeline, component


@pipeline(name="DiabetesPredictionPipeline")
def DiabetesPredictionPipeline(nas_mount_path):
    """
    This pipeline performs diabetes prediction using a RandomForestClassifier.

    Args:
    nas_mount_path (str): The path to the data on a Network Attached Storage (NAS).

    Returns:
    Artifact: A CSV file containing preprocessed data.
    """
    # Load data from NAS
    load_data = component.load_data(
        nas_mount_path,
        artifact_name="diabetes_data",
        description="Load diabetes data from NAS",
    )

    # Train a RandomForestClassifier
    train_model = component.train_random_forest_classifier(
        load_data.output,
        artifact_name="diabetes_model",
        description="Train a RandomForestClassifier",
    )

    # Make predictions
    predict_model = component.predict_random_forest_classifier(
        train_model.output,
        artifact_name="diabetes_predictions",
        description="Make predictions",
    )

    return predict_model.output
