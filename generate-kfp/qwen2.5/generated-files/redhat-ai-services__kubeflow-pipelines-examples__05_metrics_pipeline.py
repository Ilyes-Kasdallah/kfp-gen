
from kfp import dsl

@dsl.pipeline(name="metrics_pipeline")
def produce_metrics():
    # Define the components
    produce_accuracy = dsl.component(
        name="produce_accuracy",
        description="Generates a JSON file with accuracy score and mse score.",
        steps=[
            dsl.output("accuracy_score", type=dsl.float),
            dsl.output("mse_score", type=dsl.float)
        ]
    )
    
    # Define the main task
    generate_metrics = dsl.task(
        name="generate_metrics",
        description="Runs the produce_accuracy component.",
        steps=[
            produce_accuracy()
        ]
    )

    # Return the main task
    return generate_metrics
