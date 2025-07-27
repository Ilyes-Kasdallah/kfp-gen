import os
import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics

# Define the pipeline root
pipeline_root = "gs://my-bucket/pipeline-root"


# Define the preprocessing component
@dsl.component
def preprocess(raw_data_dir: str, processed_data_dir: str):
    # Load raw image data
    raw_images = [os.path.join(raw_data_dir, f"image_{i}.jpg") for i in range(10)]

    # Preprocess images
    # Example: Resize images to 224x224
    for img_path in raw_images:
        # Open image
        with open(img_path, "rb") as f:
            img_data = f.read()

        # Resize image
        resized_img = cv2.resize(img_data, (224, 224))

        # Save processed image
        processed_img_path = os.path.join(processed_data_dir, f"image_{i}_resized.jpg")
        cv2.imwrite(processed_img_path, resized_img)

    # Save processed images to output directory
    for img_path in raw_images:
        processed_img_path = os.path.join(processed_data_dir, f"image_{i}_resized.jpg")
        os.rename(img_path, processed_img_path)


# Define the classification component
@dsl.component
def classify(image_path: str, model: Model):
    # Load preprocessed image
    with open(image_path, "rb") as f:
        img_data = f.read()

    # Load model
    model = Model.from_pretrained(model.name)

    # Make prediction
    predictions = model.predict(img_data)

    # Return predictions
    return predictions


# Define the pipeline
@dsl.pipeline(name="End2end Resnet50 Classification")
def end2end_resnet50_classification(
    raw_data_dir: str, processed_data_dir: str, model_name: str
):
    # Preprocess images
    preprocess(raw_data_dir, processed_data_dir)

    # Classify images
    predictions = classify(processed_data_dir, model_name)

    # Output results
    Output("predictions", predictions)


# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiler.compile(end2end_resnet50_classification, pipeline_root=pipeline_root)
