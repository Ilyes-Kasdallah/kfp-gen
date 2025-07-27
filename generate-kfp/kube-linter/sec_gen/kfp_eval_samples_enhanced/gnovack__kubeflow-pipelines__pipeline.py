import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Boston Housing Pipeline")
def BostonHousingPipeline():
    # Preprocess Data
    x_train = component(
        name="preprocess_data",
        inputs={
            "image": Input(Dataset("gnovack/boston_pipeline_preprocessing:latest"))
        },
        outputs={"x_train": Output(Dataset("x_train.npy"))},
        steps=[
            component(
                name="load_image",
                inputs={
                    "image": Input(
                        Dataset("gnovack/boston_pipeline_preprocessing:latest")
                    )
                },
                outputs={"image": Output(Dataset("image.npy"))},
            ),
            component(
                name="resize_image",
                inputs={"image": Input(Dataset("image.npy"))},
                outputs={"image": Output(Dataset("resized_image.npy"))},
            ),
            component(
                name="normalize_image",
                inputs={"image": Input(Dataset("resized_image.npy"))},
                outputs={"image": Output(Dataset("normalized_image.npy"))},
            ),
        ],
    )

    # Train the Model
    model = component(
        name="train_model",
        inputs={
            "x_train": Input(Dataset("x_train.npy")),
            "y_train": Input(Dataset("y_train.")),
        },
        outputs={"model": Output(Model("model.h5"))},
        steps=[
            component(
                name="load_model",
                inputs={"model": Input(Model("model.h5"))},
                outputs={"model": Output(Model("model.h5"))},
            ),
            component(
                name="train_model",
                inputs={"model": Input(Model("model.h5"))},
                outputs={"model": Output(Model("model.h5"))},
            ),
        ],
    )

    # Evaluate the Model
    metrics = component(
        name="evaluate_model",
        inputs={"model": Input(Model("model.h5"))},
        outputs={"metrics": Output(Metrics())},
        steps=[
            component(
                name="predict",
                inputs={"model": Input(Model("model.h5"))},
                outputs={"predictions": Output(Dataset("predictions.npy"))},
            )
        ],
    )

    # Save the Model
    save_model = component(
        name="save_model",
        inputs={"model": Input(Model("model.h5"))},
        outputs={"model": Output(Model("model.h5"))},
        steps=[
            component(
                name="save_model",
                inputs={"model": Input(Model("model.h5"))},
                outputs={"model": Output(Model("model.h5"))},
            )
        ],
    )

    # Deploy the Model
    deploy_model = component(
        name="deploy_model",
        inputs={"model": Input(Model("model.h5"))},
        outputs={"deployment_id": Output(str())},
        steps=[
            component(
                name="deploy_model",
                inputs={"model": Input(Model("model.h5"))},
                outputs={"deployment_id": Output(str())},
            )
        ],
    )

    # Run the Pipeline
    pipeline_root = "gs://my-bucket/pipeline-root"
    pipeline(
        pipeline_root=pipeline_root,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        model=model,
        metrics=metrics,
        save_model=save_model,
        deploy_model=deploy_model,
    )
