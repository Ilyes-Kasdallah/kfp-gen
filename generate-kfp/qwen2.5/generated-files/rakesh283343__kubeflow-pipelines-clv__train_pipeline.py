
from kfp import dsl

@dsl.pipeline(name="CLV Training")
def CLV_Training():
    # Load sales transactions data
    load_sales_transactions = dsl.component(
        name="load_sales_transactions",
        description="Load sales transactions data.",
        inputs={
            "sales_data": dsl.input("sales_data")
        },
        outputs={
            "sales_dataset": dsl.output("sales_dataset")
        }
    )

    # Train CLV model
    train_clv_model = dsl.component(
        name="train_clv_model",
        description="Train CLV model.",
        inputs={
            "sales_dataset": dsl.input("sales_dataset")
        },
        outputs={
            "clv_model": dsl.output("clv_model")
        }
    )

    # Evaluate CLV model
    evaluate_clv_model = dsl.component(
        name="evaluate_clv_model",
        description="Evaluate CLV model.",
        inputs={
            "clv_model": dsl.input("clv_model")
        },
        outputs={
            "evaluation_results": dsl.output("evaluation_results")
        }
    )

    return {
        "load_sales_transactions": load_sales_transactions,
        "train_clv_model": train_clv_model,
        "evaluate_clv_model": evaluate_clv_model
    }
