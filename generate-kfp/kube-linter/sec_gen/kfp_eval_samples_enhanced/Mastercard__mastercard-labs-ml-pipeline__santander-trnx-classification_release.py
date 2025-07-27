import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Santander Customer Transaction Prediction Release Pipeline")
def santander_customer_transaction_prediction_release_pipeline(platform="GCP"):
    # Define the Deployment Component
    deployment_component = component(
        name="DeploymentComponent",
        description="Deploying a machine learning model to predict customer transactions.",
        inputs={
            "model": Input[Model](name="model"),
            "data": Input[Dataset](name="data"),
            "platform": Input[str](name="platform"),
        },
        outputs={
            "deployment_id": Output[str](name="deployment_id"),
            "status": Output[Metrics](name="status"),
        },
        steps=[
            # Step 1: Load the model
            dsl.component(
                name="LoadModel",
                description="Loading the machine learning model from a specified location.",
                inputs={"model_location": Input[str](name="model_location")},
                outputs={"model": Output[Model](name="model")},
            ),
            # Step 2: Prepare the data
            dsl.component(
                name="PrepareData",
                description="Preparing the input data for the model.",
                inputs={"data": Input[Dataset](name="data")},
                outputs={"prepared_data": Output[Dataset](name="prepared_data")},
            ),
            # Step 3: Train the model
            dsl.component(
                name="TrainModel",
                description="Training the machine learning model.",
                inputs={
                    "model": Input[Model](name="model"),
                    "prepared_data": Input[Dataset](name="prepared_data"),
                },
                outputs={"trained_model": Output[Model](name="trained_model")},
            ),
            # Step 4: Deploy the model
            dsl.component(
                name="DeployModel",
                description="Deploying the trained model to a specified platform.",
                inputs={
                    "model": Input[Model](name="trained_model"),
                    "platform": Input[str](name="platform"),
                },
                outputs={
                    "deployment_id": Output[str](name="deployment_id"),
                    "status": Output[Metrics](name="status"),
                },
            ),
        ],
        retries=2,
        resource_limits={"cpu": "1", "memory": "1Gi"},
    )

    # Define the Web Application Launch Component
    web_application_launch_component = component(
        name="WebApplicationLaunchComponent",
        description="Launching the web application using the deployed model.",
        inputs={
            "deployment_id": Input[str](name="deployment_id"),
            "model": Input[Model](name="trained_model"),
        },
        outputs={"web_app_url": Output[str](name="web_app_url")},
    )

    # Define the pipeline
    pipeline = pipeline(
        name="SantanderCustomerTransactionPredictionReleasePipeline",
        steps=[deployment_component, web_application_launch_component],
    )

    # Return the pipeline root
    return pipeline_root
