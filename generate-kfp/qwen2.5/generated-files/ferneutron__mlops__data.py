
from kfp import dsl

@dsl.pipeline(name="iris_pipeline")
def iris_pipeline(project_id, bq_dataset):
    # Load data from BigQuery
    load_data = dsl.component(
        name="load_data",
        description="Load data from BigQuery",
        inputs={
            "project_id": dsl.Input("project_id", type=dsl.String),
            "bq_dataset": dsl.Input("bq_dataset", type=dsl.String)
        },
        outputs={
            "data": dsl.Output("data", type=dsl.Table)
        },
        steps=[
            dsl.LoadTable(
                source=f"bigquery://{project_id}.{bq_dataset}",
                destination="data"
            )
        ]
    )

    # Perform machine learning on the loaded data
    model_training = dsl.component(
        name="model_training",
        description="Train a machine learning model",
        inputs={
            "data": dsl.Input("data", type=dsl.Table)
        },
        outputs={
            "model": dsl.Output("model", type=dsl.Table)
        },
        steps=[
            dsl.ModelTraining(
                model_name="iris_model",
                input_table="data",
                output_table="model"
            )
        ]
    )

    # Deploy the trained model
    deploy_model = dsl.component(
        name="deploy_model",
        description="Deploy the trained model",
        inputs={
            "model": dsl.Input("model", type=dsl.Table)
        },
        outputs={
            "deployment_id": dsl.Output("deployment_id", type=dsl.String)
        },
        steps=[
            dsl.DeployModel(
                deployment_id="iris_deployment",
                model_name="iris_model",
                deployment_type="gcp"
            )
        ]
    )

    return load_data, model_training, deploy_model
