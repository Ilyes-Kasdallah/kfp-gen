from kfp.compiler import Compiler

from kfp import dsl

from src.pipelines.training_model.training_pipeline import model_training_component
from src.pipelines.validation_model.validation_pipeline import model_validation_with_serializable_metrics
from src.pipelines.data_ingestion.ingestion_pipeline import data_ingestion_component
from src.pipelines.serving_model.serving_model import deploy_model_with_kserve_sdk

env = {
    "minio_bucket": "titanic-model",
    "minio_endpoint": "minio.kubeflow:9000",
    "minio_access_key": "minio",
    "minio_secret_key": "minio123"
    
}

@dsl.pipeline(
    name='Titanic Survival Prediction Pipeline',
    description='Pipeline for training and validating a Titanic survival prediction model'
)

def titanic_pipeline(
        dataset_url: str,
        output_dir: str,
        test_size: float = 0.2,
        random_state: int = 42
):
    
    data_task = data_ingestion_component(
        dataset_url=dataset_url,
        output_dir=output_dir,
        minio_access_key=env["minio_access_key"],
        minio_secret_key=env["minio_secret_key"],
        minio_endpoint=env["minio_endpoint"],
    )

    model_task = model_training_component(
        train_data_dir=data_task.output,
        random_state=random_state,
        output_dir=output_dir,
        minio_access_key=env["minio_access_key"],
        minio_secret_key=env["minio_secret_key"],
        minio_endpoint=env["minio_endpoint"],
        test_size=test_size,
        
    )

    validation_task = model_validation_with_serializable_metrics(
        model_path=model_task.output,
        test_data_dir=data_task.output,
        minio_access_key=env["minio_access_key"],
        minio_secret_key=env["minio_secret_key"],
        minio_endpoint=env["minio_endpoint"],
        test_size=test_size,
    )
    
    deploy_task = deploy_model_with_kserve_sdk(
        minio_access_key=env["minio_access_key"],
        minio_endpoint=env["minio_endpoint"],
        minio_secret_key=env["minio_secret_key"],
        model_bucket=env["minio_bucket"],
        model_key=model_task.output,
        model_name="logistic_model.pkl",
        namespace="kubeflow",
        
    )
    deploy_task.after(validation_task)
# Create a pipeline run

def main():
    """
    Compile the pipeline to YAML and optionally run it.
    """

    # Compile the pipeline
    pipeline_filename = 'titanic_pipeline.yaml'
    Compiler().compile(
        pipeline_func=titanic_pipeline,
        package_path=pipeline_filename
    )

    print(f"Pipeline compiled successfully to {pipeline_filename}")


if __name__ == '__main__':
    main()
