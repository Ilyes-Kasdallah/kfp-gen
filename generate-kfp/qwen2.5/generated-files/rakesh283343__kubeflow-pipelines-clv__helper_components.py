
from kfp import dsl

@dsl.pipeline(name="sales_pipeline")
def sales_pipeline():
    # Load transactions from BigQuery
    load_transactions = dsl.component(
        name="load_transactions",
        description="Loads historical sales transactions into a BigQuery table.",
        inputs={
            "transactions_table": dsl.Input("transactions_table"),
        },
        outputs={
            "sales_table": dsl.Output("sales_table"),
        },
        steps=[
            dsl.Load(
                source="bigquery",
                table="sales_transactions",
                schema="sales_transaction",
                columns=["transaction_id", "customer_id", "sale_date", "amount"],
            ),
        ],
    )

    # Predict CLV
    predict_clv = dsl.component(
        name="predict_clv",
        description="Predicts customer lifetime value (CLV) for each transaction.",
        inputs={
            "sales_table": dsl.Input("sales_table"),
        },
        outputs={
            "clv_table": dsl.Output("clv_table"),
        },
        steps=[
            dsl.SQL(
                sql="SELECT customer_id, amount, SUM(amount * (sale_date - transaction_date)) AS total_amount_sold"
                "FROM sales_transactions"
                "GROUP BY customer_id, sale_date",
            ),
            dsl.SQL(
                sql="SELECT customer_id, total_amount_sold, CAST(SUM(amount * (sale_date - transaction_date)) AS REAL) / COUNT(transaction_id) AS clv"
                "FROM sales_transactions"
                "GROUP BY customer_id, sale_date",
            ),
        ],
    )

    return load_transactions, predict_clv
