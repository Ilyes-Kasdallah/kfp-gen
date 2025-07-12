```python
import kfp
from kfp import dsl

# Load data component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn"],
)
def load_data(url1: str, url2: str) -> dsl.Artifact:
    # Load data from URLs
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)

    # Perform data cleaning and preprocessing
    df1.dropna(inplace=True)
    df1['gender'] = df1['gender'].map({'Male': 0, 'Female': 1})

    return dsl.Artifact(type=dsl.ArtifactType.DATAFRAME, uri=df1.to_csv(index=False))

# Prepare data component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "scikit-learn"],
)
def prepare_data(data: dsl.Artifact) -> dsl.Artifact:
    # Load preprocessed data
    df = pd.read_csv(data.uri)

    # Split data into training and testing sets
    X = df.drop('target', axis=1)
    y = df['target']
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save training and testing sets as separate CSV files
    x_train.to_csv("x_train.csv", index=False)
    x_test.to_csv("x_test.csv", index=False)
    y_train.to_csv("y_train.csv", index=False)
    y_test.to_csv("y_test.csv", index=False)

    return dsl.Artifact(type=dsl.ArtifactType.DATAFRAME, uri="x_train.csv"), \
           dsl.Artifact(type=dsl.ArtifactType.DATAFRAME, uri="x_test.csv"), \
           dsl.Artifact(type=dsl.ArtifactType.DATAFRAME, uri="y_train.csv"), \
           dsl.Artifact(type=dsl.ArtifactType.DATAFRAME, uri="y_test.csv")

# Main pipeline
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data
    load_data_task = load_data(url1="https://raw.githubusercontent.com/kubeflow/pipelines/HEAD/docs/tutorials/data-science/diabetes/load_data_1.csv",
                               url2="https://raw.githubusercontent.com/kubeflow/pipelines/HEAD/docs/tutorials/data-science/diabetes/load_data_2.csv")

    # Prepare data
    prepare_data_task = prepare_data(load_data_task.outputs.data)

# Compile and run the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(diabetes_prediction_pipeline, "kubeflowPipeline0722.yaml")
    kfp.Client().create_run_from_pipeline_package("kubeflowPipeline0722.yaml", arguments={})
```

This code snippet defines a Kubeflow Pipeline named `diabetes_prediction_pipeline` that performs diabetes prediction. It includes two components: `load_data` and `prepare_data`. The `load_data` component loads data from two CSV files, cleans it, and converts categorical features to numerical representations. The `prepare_data` component splits the data into training and testing sets and saves them as separate CSV files. The pipeline's control flow is sequential, with `prepare_data` running after `load_data`. The pipeline uses the `kfp` library for pipeline definition and `dsl` for component definition and orchestration.