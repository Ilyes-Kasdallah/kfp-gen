
from kfp import dsl

@dsl.pipeline(name="optuna pipeline")
def optuna_pipeline(pipeline_name):
    # Define the components
    optuna_worker = dsl.component(
        name="optuna-worker",
        description="Runs the hyperparameter optimization process using Optuna.",
        inputs={
            "pipeline_name": dsl.Input("pipeline_name", type=dsl.String())
        },
        outputs={
            "best_params": dsl.Output("best_params", type=dsl.Dict())
        },
        steps=[
            dsl.task(
                name="run_optuna",
                description="Runs the hyperparameter optimization process using Optuna.",
                inputs={
                    "pipeline_name": dsl.Input("pipeline_name", type=dsl.String())
                },
                outputs={
                    "best_params": dsl.Output("best_params", type=dsl.Dict())
                },
                steps=[
                    dsl.task(
                        name="optimize_hyperparameters",
                        description="Optimizes the hyperparameters of the pipeline.",
                        inputs={
                            "pipeline_name": dsl.Input("pipeline_name", type=dsl.String())
                        },
                        outputs={
                            "best_params": dsl.Output("best_params", type=dsl.Dict())
                        }
                    )
                ]
            )
        ]
    )

    return optuna_worker
