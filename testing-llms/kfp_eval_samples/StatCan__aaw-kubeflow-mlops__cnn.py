```python
import kfp
from kfp.components import component
from kfp.dsl import pipeline

# Import necessary libraries
import os
import subprocess

# Define the Exit Handler component
@component(
    base_image="k8scc01covidmlopsacr.azurecr.io/mlops/python",
    packages_to_install=["requests"],
)
def exit_handler():
    # Send a completion message to the callback URL
    curl_command = f"curl -X POST http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080?event_type=TRAIN_FINISH_EVENT&github_sha={os.getenv('GITHUB_SHA')}&pr_num={os.getenv('PR_NUM')}&run_id={os.getenv('KUBEFLOW_RUN_ID')}"
    subprocess.run(curl_command, shell=True)

# Define the callback component
@component(
    base_image="k8scc01covidmlopsacr.azurecr.io/mlops/python",
    packages_to_install=["requests"],
)
def callback():
    # Send a start message to the callback URL
    curl_command = f"curl -X POST http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080?event_type=TRAIN_START_EVENT&github_sha={os.getenv('GITHUB_SHA')}&pr_num={os.getenv('PR_NUM')}&run_id={os.getenv('KUBEFLOW_RUN_ID')}"
    subprocess.run(curl_command, shell=True)

# Define the tensorflow preprocess component
@component(
    base_image="k8scc01covidmlopsacr.azurecr.io/mlops/tensorflow-preprocess:latest",
    packages_to_install=["pandas", "numpy"],
    outputs=[
        {"name": "preprocessed_dataset", "type": "Artifact"}
    ],
    requirements=[
        {
            "package_name": "requests",
            "pip_version": "20.2.2"
        }
    ]
)
def tensorflow_preprocess(resource_group, workspace, dataset, token):
    # Preprocess data for CNN training
    base_path = "/mnt/azure"
    data_folder = "train"
    target_file = "train.txt"
    image_size = 160
    dataset_zip_file = "data_download"

    # Run the preprocessing script
    subprocess.run([
        "python",
        "/scripts/data.py",
        "--base-path",
        base_path,
        "--data-folder",
        data_folder,
        "--target-file",
        target_file,
        "--image-size",
        str(image_size),
        "--dataset-zip-file",
        dataset_zip_file
    ])

    # Return the preprocessed dataset artifact
    return {"preprocessed_dataset": {"path": f"{base_path}/{data_folder}/train"}}

# Define the tensorflow training component
@component(
    base_image="k8scc01covidmlopsacr.azurecr.io/mlops/tensorflow-training:latest",
    packages_to_install=["pandas", "numpy"],
    outputs=[
        {"name": "trained_model", "type": "Model"}
    ],
    requirements=[
        {
            "package_name": "requests",
            "pip_version": "20.2.2"
        }
    ]
)
def tensorflow_training(preprocessed_dataset, num_epochs, batch_size, model_name):
    # Train the CNN model
    base_path = "/mnt/azure"
    data_directory = "train"

    # Run the training script
    subprocess.run([
        "python",
        "/scripts/train.py",
        "--base-path",
        base_path,
        "--data-directory",
        data_directory,
        "--num-epochs",
        str(num_epochs),
        "--batch-size",
        str(batch_size),
        "--model-name",
        model_name
    ])

    # Return the trained model artifact
    return {"trained_model": {"path": f"{base_path}/{data_directory}/model.h5"}}

# Define the pipeline
@cnn
def cnn_pipeline(
    resource_group,
    workspace,
    dataset,
    token,
    use_azstorage_secret=False,
    num_epochs=2,
    batch_size=32,
    model_name="cnnmodel"
):
    # Initialize the callback container
    callback_container = callback()

    # Preprocess the data
    preprocess_output = tensorflow_preprocess(
        resource_group=resource_group,
        workspace=workspace,
        dataset=dataset,
        token=token
    )

    # Train the model
    train_output = tensorflow_training(
        pretrained_dataset=preprocess_output["preprocessed_dataset"],
        num_epochs=num_epochs,
        batch_size=batch_size,
        model_name=model_name
    )

    # Exit the pipeline
    exit_handler()

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(cnn_pipeline, package_path="cnn.yaml")
```

This code defines a Kubeflow Pipeline named `Tacos vs. Burritos` that performs CNN training using the specified components. The pipeline includes an Exit Handler, a callback, a tensorflow preprocess component, and a tensorflow training component. The pipeline uses the Kubeflow Pipelines SDK and leverages Docker images and command-line arguments for preprocessing and training.