```python
from kfp import dsl
import pandas as pd
from google.cloud import bigquery
from sklearn.model_selection import train_test_split

# Load data from BigQuery
@dsl.component(
    base_image="gcr.io/deeplearning-platform-release/tf2-cpu.2-6:latest",
    outputs=["train_dataset", "test_dataset"]
)
def load_data(project_id: str, bq_dataset: str, bq_table: str):
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM {bq_dataset}.{bq_table}"
    df = client.query(query).to_dataframe()

    # Preprocess 'Species' column
    df['Species'] = df['Species'].map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df.drop('Species', axis=1), df['Species'], test_size=0.2, random_state=42)

    # Save datasets to CSV files
    X_train.to_csv("train.csv", index=False)
    X_test.to_csv("test.csv", index=False)

    return "train.csv", "test.csv"

# Define the main pipeline
@dsl.pipeline(name="iris_pipeline")
def iris_pipeline():
    load_data_task = load_data(project_id="your-project-id", bq_dataset="your-dataset", bq_table="your-table")

    # Add more components here if needed
```

In this solution, we define a Kubeflow Pipeline named `iris_pipeline` that includes a single component `load_data`. The `load_data` component connects to a Google BigQuery table, splits the data into training and testing sets, preprocesses the 'Species' column, and saves the datasets as CSV files. The pipeline is defined using the `@dsl.pipeline` decorator and includes the `load_data` component as its entry point. Additional components can be added as needed to perform further steps in the machine learning workflow.