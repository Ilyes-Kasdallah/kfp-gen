
from kfp import dsl

@dsl.pipeline(name="Exit Handler")
def Exit_Handler(
    url: str,
    legacy_exit_handler: str = "legacy_exit_handler",
):
    # Define the GCS download component
    download_component = dsl.component(
        name="GCS - Download",
        image="gcr.io/google-cloud-sdk/279.0.0/gcs-download",
        args=[
            "--bucket", "your-bucket-name",
            "--object", url,
            "--output", "downloaded-file.txt"
        ],
        outputs={
            "downloaded_file.txt": dsl.output()
        }
    )

    # Define the legacy exit handler component
    legacy_exit_handler_component = dsl.component(
        name=legacy_exit_handler,
        image="legacy_exit_handler_image",
        args=["exit"]
    )

    # Define the main component that will run the download and legacy exit handler
    main_component = dsl.component(
        name="Main Component",
        steps=[
            download_component,
            legacy_exit_handler_component
        ]
    )

    return main_component
