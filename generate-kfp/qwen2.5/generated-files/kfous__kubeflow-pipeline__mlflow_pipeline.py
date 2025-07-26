
from kfp import dsl

@dsl.pipeline(name="MLflow Logging Pipeline")
def mlflow_logging_pipeline():
    # Install the mlflow library
    mlflow.__version__
    
    # Set the tracking URI to http://host.docker
    mlflow.set_tracking_uri("http://host.docker")

    # Define the component to log parameters and metrics
    @dsl.component
    def mlflow_logging_op(params):
        # Log parameters to MLflow
        mlflow.log_params(params)
        
        # Log metrics to MLflow
        mlflow.log_metric("accuracy", params["accuracy"])
        mlflow.log_metric("precision", params["precision"])

# Example usage of the pipeline
mlflow_logging_pipeline()
