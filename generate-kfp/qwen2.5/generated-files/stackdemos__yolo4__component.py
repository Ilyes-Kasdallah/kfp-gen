
from kfp import dsl

@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Define the download-artifact component
    download_artifact = dsl.component(
        name="download-artifact",
        image="appropriate/curl",
        command=["curl", "-o", "output.txt", "https://example.com/file.zip"],
        inputs=[
            dsl.input("url", type=dsl.string),
            dsl.input("expected_md5", type=dsl.string)
        ],
        outputs=[
            dsl.output("downloaded_file", type=dsl.string)
        ]
    )

    # Define the model training component
    model_training = dsl.component(
        name="model-training",
        image="appropriate/model-training",
        command=["python", "train_model.py", "--input-file", "downloaded_file.txt", "--expected-md5", "expected_md5"]
    )

    # Connect the components
    download_artifact >> model_training
