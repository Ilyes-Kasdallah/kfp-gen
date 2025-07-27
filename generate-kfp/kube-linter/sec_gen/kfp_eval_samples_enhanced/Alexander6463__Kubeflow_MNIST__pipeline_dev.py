import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="End-to-End MNIST Pipeline")
def end_to_end_mnist_pipeline(
    # Define the input parameters
    input_bucket="pipelines-tutorial-data",
    # Define the output parameters
    output_dataset="output-dataset",
    output_model="output-model",
    # Define the pipeline steps
    download_dataset=component(
        name="Download Dataset",
        description="Downloads a dataset from the specified bucket.",
        inputs={
            "input_bucket": Input(bucket=input_bucket),
        },
        outputs={
            "output_dataset": Output(dataset=output_dataset),
        },
        steps=[
            dsl.DownloadObject(
                object_name="datasets.tar.gz",
                source_path="gs://{input_bucket}/datasets.tar.gz",
            ),
        ],
    ),
    model_training=component(
        name="Model Training",
        description="Trains a model on the downloaded dataset.",
        inputs={
            "input_dataset": Input(dataset=output_dataset),
        },
        outputs={
            "output_model": Output(model=output_model),
        },
        steps=[
            dsl.ModelTraining(
                model_name="mnist_model",
                input_data="input_dataset",
                output_dir="gs://{output_bucket}/model",
            ),
        ],
    ),
    evaluation=component(
        name="Evaluation",
        description="Evaluates the model's performance on the test dataset.",
        inputs={
            "input_dataset": Input(dataset=output_dataset),
        },
        outputs={
            "output_metrics": Output(metrics=Metrics()),
        },
        steps=[
            dsl.Evaluation(
                model_name="mnist_model",
                input_data="input_dataset",
                output_dir="gs://{output_bucket}/evaluation",
            ),
        ],
    ),
    export=component(
        name="Export",
        description="Exports the trained model to a Google Cloud Storage bucket.",
        inputs={
            "input_model": Input(model=output_model),
        },
        outputs={
            "output_export_dir": Output(directory="gs://{output_bucket}/export"),
        },
        steps=[
            dsl.ExportModel(
                model_name="mnist_model",
                output_dir="gs://{output_bucket}/export",
            ),
        ],
    ),
    deployment=component(
        name="Deployment",
        description="Deploys the model to a Kubernetes cluster.",
        inputs={
            "input_model": Input(model=output_model),
        },
        outputs={
            "output_kubernetes_pod": Output(pod_name="kubernetes-pod"),
        },
        steps=[
            dsl.KubernetesPod(
                image="gcr.io/kubeflow/pipelines:v2",
                command=[
                    "bash",
                    "-c",
                    "kubectl apply -f gs://{output_bucket}/deployment.yaml",
                ],
                env={"KUBEFLOW_POD_NAME": "kubernetes-pod"},
            ),
        ],
    ),
):

    # Call the components with the provided inputs
    download_dataset(input_bucket=input_bucket)
    model_training(input_dataset=input_dataset)
    evaluation(input_dataset=input_dataset)
    export(output_export_dir=output_export_dir)
    deployment(output_kubernetes_pod=output_kubernetes_pod)
