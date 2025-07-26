
from kfp import dsl

@dsl.pipeline(name="The-Iris-Pipeline-v1")
def iris_pipeline(project_id, bq_dataset, bq_table):
    # Load data from BigQuery
    load_data = dsl.component(
        name="load_data",
        description="Loads data from BigQuery",
        inputs={
            "project_id": dsl.InputParameter("project_id"),
            "bq_dataset": dsl.InputParameter("bq_dataset"),
            "bq_table": dsl.InputParameter("bq_table")
        },
        outputs={
            "train_dataset": dsl.OutputParameter("train_dataset"),
            "test_dataset": dsl.OutputParameter("test_dataset")
        },
        steps=[
            dsl.LoadFromBigQuery(
                project=project_id,
                dataset=bq_dataset,
                table=bq_table
            )
        ]
    )

    # Train the model
    train_model = dsl.component(
        name="train_model",
        description="Trains the model",
        inputs={
            "train_dataset": dsl.InputParameter("train_dataset")
        },
        outputs={
            "model": dsl.OutputParameter("model")
        },
        steps=[
            dsl.ModelTraining(
                model_name="iris_model",
                input_columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
                output_columns=["prediction"]
            )
        ]
    )

    # Evaluate the model
    evaluate_model = dsl.component(
        name="evaluate_model",
        description="Evaluates the model",
        inputs={
            "model": dsl.InputParameter("model")
        },
        outputs={
            "accuracy": dsl.OutputParameter("accuracy")
        },
        steps=[
            dsl.ModelEvaluation(
                model_name="iris_model",
                input_columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
                expected_output=0.85
            )
        ]
    )

    return {
        "load_data": load_data,
        "train_model": train_model,
        "evaluate_model": evaluate_model
    }
