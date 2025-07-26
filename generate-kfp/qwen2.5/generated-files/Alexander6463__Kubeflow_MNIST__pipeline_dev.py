
from kfp import pipeline
from kfp.components import DownloadDataset, ModelTraining, EvaluateModel, ExportModel, DeployModel

@dsl.pipeline(name="End-to-End MNIST Pipeline", description="End-to-End Machine Learning Pipeline")
def EndToEndMNISTPipeline():
    # Download the dataset
    download_dataset = DownloadDataset(
        name="datasets.tar.gz",
        bucket="pipelines-tutorial-data",
        source_path="https://raw.githubusercontent.com/keras-team/mnist/master/data/mnist.tgz"
    )

    # Model training
    model_training = ModelTraining(
        name="model-training",
        model_name="mnist_model",
        dataset=download_dataset.outputs["dataset"],
        epochs=5,
        batch_size=32
    )

    # Evaluate the model
    evaluate_model = EvaluateModel(
        name="evaluate-model",
        model=model_training.outputs["model"],
        dataset=download_dataset.outputs["dataset"]
    )

    # Export the model
    export_model = ExportModel(
        name="export-model",
        model=model_training.outputs["model"],
        output_path="exported_model"
    )

    # Deploy the model
    deploy_model = DeployModel(
        name="deploy-model",
        model=model_training.outputs["model"],
        namespace="default",
        deployment_config={
            "replicas": 1,
            "image": "tensorflow/tensorflow:2.8.0-py3.8",
            "port": 8080
        }
    )

# Define the pipeline function
@dsl.function(name="pipeline_dev")
def pipeline_dev():
    return EndToEndMNISTPipeline()

# Run the pipeline
pipeline.run()
