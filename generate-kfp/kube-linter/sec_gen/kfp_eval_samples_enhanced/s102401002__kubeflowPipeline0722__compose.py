import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Data_Processing_and_Hyperparameter_Tuning")
def Data_Processing_and_Hyperparameter_Tuning(
    input_data: Input[Dataset],
    model: Model,
    hyperparameters: dict,
    output_dataset: Output[Dataset],
    output_model: Output[Model],
    cache_key: Output[str],
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Step 1: Data Preprocessing
    preprocess_step = component(
        name="Preprocess",
        inputs={"input_data": input_data},
        outputs={"output_dataset": output_dataset},
        steps=[dsl.Copy(src=input_data, dst=output_dataset)],
    )

    # Step 2: Hyperparameter Optimization
    optimize_step = component(
        name="Optimize",
        inputs={"model": model, "hyperparameters": hyperparameters},
        outputs={"output_model": output_model},
        steps=[
            dsl.Run(
                python_callable=kfp.components.run,
                args=[
                    "--model",
                    model.name,
                    "--hyperparameters",
                    json.dumps(hyperparameters),
                    "--output-model",
                    output_model.name,
                ],
                retries=retries,
                resource_limits=resource_limits,
            )
        ],
    )

    # Step 3: Cache and Retries
    cache_step = component(
        name="Cache",
        inputs={"cache_key": cache_key},
        outputs={"output_dataset": output_dataset},
        steps=[dsl.Cache(key=cache_key, ttl=3600)],  # Cache for 1 hour
    )

    # Step 4: Run the pipeline
    run_pipeline = component(
        name="Run Pipeline",
        inputs={
            "input_data": input_data,
            "model": model,
            "hyperparameters": hyperparameters,
            "output_dataset": output_dataset,
            "output_model": output_model,
            "cache_key": cache_key,
            "retries": retries,
            "resource_limits": resource_limits,
        },
        outputs={"output_metrics": metrics},
        steps=[preprocess_step, optimize_step, cache_step, run_pipeline],
    )

    return run_pipeline
