
from kfp import dsl

@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Define the download-artifact component
    download_artifact = dsl.component(
        name="download-artifact",
        description="Downloads a data artifact from a URL and writes it to a specified path.",
        inputs={
            "url": dsl.input("url", type=str),
            "expected_md5": dsl.input("expected_md5", type=str)
        },
        outputs={
            "downloaded_file": dsl.output("downloaded_file", type=str)
        },
        steps=[
            dsl.step(
                name="download_data",
                task_id="download_data",
                image="your-docker-image",
                command=["curl", "-o", "downloaded_file", f"{url}"]
            ),
            dsl.step(
                name="validate_checksum",
                task_id="validate_checksum",
                image="your-docker-image",
                command=["md5sum", "downloaded_file", "--checksum", f"{expected_md5}"]
            )
        ]
    )

    # Define the model training component
    model_training = dsl.component(
        name="model_training",
        description="Trains a model using the downloaded data.",
        inputs={
            "downloaded_file": dsl.input("downloaded_file", type=str)
        },
        outputs={
            "trained_model": dsl.output("trained_model", type=str)
        },
        steps=[
            dsl.step(
                name="train_model",
                task_id="train_model",
                image="your-docker-image",
                command=["python", "train_model.py", downloaded_file]
            )
        ]
    )

    # Connect the components
    download_artifact >> model_training
